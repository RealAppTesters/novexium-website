from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class Invoice(BaseModel):
    __tablename__ = "invoices"
    
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    stripe_invoice_id = Column(String(255), nullable=True, unique=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(String(20), default="pending")  # pending, paid, failed, refunded
    invoice_date = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    paid_date = Column(DateTime(timezone=True), nullable=True)
    pdf_url = Column(String(500), nullable=True)
    items = Column(JSON, nullable=True)  # Line items
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")
    user = relationship("User")
    
    __table_args__ = (
        Index('idx_invoice_user', 'user_id'),
        Index('idx_invoice_status', 'status'),
        Index('idx_invoice_date', 'invoice_date'),
    )
