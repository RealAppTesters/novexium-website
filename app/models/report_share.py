from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ReportShare(BaseModel):
    __tablename__ = "report_shares"
    
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False, index=True)
    share_token = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    max_views = Column(Integer, nullable=True)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    report = relationship("Report")
    
    __table_args__ = (
        Index('idx_share_token', 'share_token'),
        Index('idx_share_active', 'is_active'),
    )
