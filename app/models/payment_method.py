from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class PaymentMethod(BaseModel):
    __tablename__ = "payment_methods"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    stripe_payment_method_id = Column(String(255), nullable=False, unique=True)
    brand = Column(String(50), nullable=True)  # visa, mastercard, amex, etc.
    last_four = Column(String(4), nullable=True)
    exp_month = Column(Integer, nullable=True)
    exp_year = Column(Integer, nullable=True)
    billing_name = Column(String(255), nullable=True)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")
    
    __table_args__ = (
        Index('idx_payment_user', 'user_id'),
        Index('idx_payment_default', 'user_id', 'is_default'),
    )
