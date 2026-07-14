from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.billing_service import BillingService

router = APIRouter(prefix="/billing", tags=["Billing"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def billing_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the billing dashboard"""
    service = BillingService(db)
    subscription = service.get_subscription(str(current_user.id))
    plans = service.get_plans()
    payment_methods = service.get_payment_methods(str(current_user.id))
    invoices = service.get_invoices(str(current_user.id))
    usage = service.get_usage(str(current_user.id))
    
    return templates.TemplateResponse(
        "billing/index.html",
        {
            "request": request,
            "subscription": subscription,
            "plans": plans,
            "payment_methods": payment_methods,
            "invoices": invoices,
            "usage": usage
        }
    )


@router.get("/plans", response_class=HTMLResponse)
async def billing_plans(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the plans page"""
    service = BillingService(db)
    subscription = service.get_subscription(str(current_user.id))
    plans = service.get_plans()
    
    return templates.TemplateResponse(
        "billing/plans.html",
        {
            "request": request,
            "subscription": subscription,
            "plans": plans
        }
    )


@router.get("/invoices", response_class=HTMLResponse)
async def billing_invoices(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the invoices page"""
    service = BillingService(db)
    invoices = service.get_invoices(str(current_user.id))
    
    return templates.TemplateResponse(
        "billing/invoices.html",
        {
            "request": request,
            "invoices": invoices
        }
    )


@router.get("/cancel", response_class=HTMLResponse)
async def billing_cancel(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the cancel confirmation page"""
    service = BillingService(db)
    subscription = service.get_subscription(str(current_user.id))
    
    return templates.TemplateResponse(
        "billing/cancel.html",
        {
            "request": request,
            "subscription": subscription
        }
    )
