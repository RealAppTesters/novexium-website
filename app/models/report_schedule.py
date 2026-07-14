from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ReportSchedule(BaseModel):
    __tablename__ = "report_schedules"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False)
    frequency = Column(String(20), nullable=False)  # daily, weekly, monthly, quarterly, custom
    schedule_data = Column(JSON, nullable=True)  # Day of week, time, etc.
    recipients = Column(JSON, nullable=True)  # List of email addresses
    last_run = Column(DateTime(timezone=True), nullable=True)
    next_run = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")
    report = relationship("Report")
    
    __table_args__ = (
        Index('idx_schedule_user', 'user_id'),
        Index('idx_schedule_next_run', 'next_run'),
    )
