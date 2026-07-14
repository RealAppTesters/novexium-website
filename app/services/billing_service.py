from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import stripe

from app.models.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from app.models.payment_method import PaymentMethod
from app.models.invoice import Invoice
from app.billing.providers.stripe import StripeProvider
from app.billing.subscription.plans import PLANS
from app.core.config import settings


class BillingService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = StripeProvider()
    
    def get_subscription(self, user_id: str) -> Dict[str, Any]:
        """Get user's subscription"""
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_([SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE])
        ).first()
        
        if not subscription:
            return self._get_default_subscription()
        
        return self._subscription_to_dict(subscription)
    
    def get_plans(self) -> List[Dict]:
        """Get all available plans"""
        plans = []
        for plan_key, plan_data in PLANS.items():
            plan = plan_data.copy()
            plan['id'] = plan_key
            plans.append(plan)
        return plans
    
    def create_subscription(self, user_id: str, plan_id: str, payment_method_id: str = None) -> Dict:
        """Create a new subscription"""
        plan = PLANS.get(plan_id)
        if not plan:
            raise ValueError(f"Invalid plan: {plan_id}")
        
        # Create Stripe customer if needed
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Get or create Stripe customer
        customer_id = self.provider.create_customer(user.email, user.full_name)
        
        # Create subscription in Stripe
        stripe_subscription = self.provider.create_subscription(
            customer_id,
            plan_id,
            payment_method_id
        )
        
        # Create local subscription
        subscription = Subscription(
            id=uuid.uuid4(),
            user_id=user_id,
            plan=plan_id,
            status=SubscriptionStatus.TRIAL,
            stripe_subscription_id=stripe_subscription['id'],
            stripe_customer_id=customer_id,
            trial_start=datetime.utcnow(),
            trial_end=datetime.utcnow() + timedelta(days=7),
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30),
            amount=plan['price'],
            currency='USD',
            next_payment_date=datetime.utcnow() + timedelta(days=7)
        )
        
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        
        return self._subscription_to_dict(subscription)
    
    def update_subscription(self, user_id: str, new_plan_id: str) -> Dict:
        """Update subscription plan"""
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_([SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE])
        ).first()
        
        if not subscription:
            raise ValueError("No active subscription found")
        
        # Update in Stripe
        self.provider.update_subscription(
            subscription.stripe_subscription_id,
            new_plan_id
        )
        
        # Update local
        new_plan = PLANS.get(new_plan_id)
        subscription.plan = new_plan_id
        subscription.amount = new_plan['price']
        subscription.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        return self._subscription_to_dict(subscription)
    
    def cancel_subscription(self, user_id: str, cancel_at_period_end: bool = True) -> Dict:
        """Cancel subscription"""
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_([SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE])
        ).first()
        
        if not subscription:
            raise ValueError("No active subscription found")
        
        # Cancel in Stripe
        self.provider.cancel_subscription(
            subscription.stripe_subscription_id,
            cancel_at_period_end
        )
        
        # Update local
        subscription.cancel_at_period_end = cancel_at_period_end
        if not cancel_at_period_end:
            subscription.status = SubscriptionStatus.CANCELLED
            subscription.canceled_at = datetime.utcnow()
        
        self.db.commit()
        
        return self._subscription_to_dict(subscription)
    
    def get_payment_methods(self, user_id: str) -> List[Dict]:
        """Get user's payment methods"""
        methods = self.db.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id,
            PaymentMethod.is_active == True
        ).all()
        
        return [self._payment_method_to_dict(m) for m in methods]
    
    def add_payment_method(self, user_id: str, payment_method_id: str) -> Dict:
        """Add a payment method"""
        # Get payment method from Stripe
        stripe_pm = self.provider.get_payment_method(payment_method_id)
        
        # Save locally
        method = PaymentMethod(
            id=uuid.uuid4(),
            user_id=user_id,
            stripe_payment_method_id=payment_method_id,
            brand=stripe_pm.get('brand'),
            last_four=stripe_pm.get('last4'),
            exp_month=stripe_pm.get('exp_month'),
            exp_year=stripe_pm.get('exp_year'),
            billing_name=stripe_pm.get('billing_name'),
            is_default=not self.db.query(PaymentMethod).filter(
                PaymentMethod.user_id == user_id,
                PaymentMethod.is_default == True
            ).first()
        )
        
        self.db.add(method)
        self.db.commit()
        self.db.refresh(method)
        
        return self._payment_method_to_dict(method)
    
    def set_default_payment_method(self, user_id: str, payment_method_id: str) -> Dict:
        """Set default payment method"""
        # Reset all defaults
        self.db.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id
        ).update({'is_default': False})
        
        # Set new default
        method = self.db.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id,
            PaymentMethod.stripe_payment_method_id == payment_method_id
        ).first()
        
        if method:
            method.is_default = True
            self.db.commit()
            return {'default': True}
        
        return {'error': 'Payment method not found'}
    
    def get_invoices(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's invoices"""
        invoices = self.db.query(Invoice).filter(
            Invoice.user_id == user_id
        ).order_by(Invoice.invoice_date.desc()).limit(limit).all()
        
        return [self._invoice_to_dict(i) for i in invoices]
    
    def get_usage(self, user_id: str) -> Dict[str, Any]:
        """Get usage for current plan"""
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_([SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE])
        ).first()
        
        plan_key = subscription.plan if subscription else 'free'
        plan = PLANS.get(plan_key, PLANS['free'])
        
        # Calculate usage (mock)
        app_count = self.db.query(App).filter(App.user_id == user_id).count()
        
        return {
            'plan': plan_key,
            'app_count': app_count,
            'app_limit': plan['app_limit'],
            'app_percentage': int((app_count / plan['app_limit']) * 100) if plan['app_limit'] > 0 else 0,
            'audit_count': 12,  # Mock
            'audit_limit': plan.get('audit_limit', 0),
            'report_count': 8,  # Mock
            'report_limit': plan.get('report_limit', 0)
        }
    
    def _subscription_to_dict(self, sub: Subscription) -> Dict:
        plan = PLANS.get(sub.plan, {})
        return {
            'id': str(sub.id),
            'plan': sub.plan,
            'plan_name': plan.get('name', sub.plan),
            'status': sub.status,
            'trial_start': sub.trial_start.isoformat() if sub.trial_start else None,
            'trial_end': sub.trial_end.isoformat() if sub.trial_end else None,
            'current_period_end': sub.current_period_end.isoformat() if sub.current_period_end else None,
            'cancel_at_period_end': sub.cancel_at_period_end,
            'amount': sub.amount,
            'currency': sub.currency
        }
    
    def _payment_method_to_dict(self, method: PaymentMethod) -> Dict:
        return {
            'id': str(method.id),
            'stripe_id': method.stripe_payment_method_id,
            'brand': method.brand,
            'last_four': method.last_four,
            'exp_month': method.exp_month,
            'exp_year': method.exp_year,
            'billing_name': method.billing_name,
            'is_default': method.is_default
        }
    
    def _invoice_to_dict(self, invoice: Invoice) -> Dict:
        return {
            'id': str(invoice.id),
            'invoice_number': invoice.invoice_number,
            'amount': invoice.amount,
            'currency': invoice.currency,
            'status': invoice.status,
            'invoice_date': invoice.invoice_date.isoformat(),
            'pdf_url': invoice.pdf_url
        }
    
    def _get_default_subscription(self) -> Dict:
        return {
            'plan': 'free',
            'plan_name': 'Free',
            'status': 'active',
            'trial_start': None,
            'trial_end': None,
            'current_period_end': None,
            'cancel_at_period_end': False,
            'amount': 0,
            'currency': 'USD'
        }
