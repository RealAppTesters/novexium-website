from sqlalchemy import Column, String, Float, DateTime, Enum, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel
import enum

class PaymentStatus(str, enum.Enum):
    PAID = "paid"
    UNPAID = "unpaid"
    PENDING = "pending"
    FAILED = "failed"
    REFUNDED = "refunded"

class Billing(BaseModel):
    __tablename__ = "billing"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    stripe_customer_id = Column(String(255), nullable=False, index=True)
    plan = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    invoice = Column(String(255), nullable=True)
    renewal_date = Column(DateTime(timezone=True), nullable=True)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Relationships
    user = relationship("User", back_populates="billing")
    
    __table_args__ = (
        Index('idx_billing_stripe_customer', 'stripe_customer_id'),
        Index('idx_billing_renewal_date', 'renewal_date'),
        Index('idx_billing_payment_status', 'payment_status'),
    )
