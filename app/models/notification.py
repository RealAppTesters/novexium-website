from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=True, index=True)
    notification_type = Column(String(50), nullable=False)  # info, success, warning, important, system, billing, security, product
    priority = Column(String(20), default="medium")  # critical, high, medium, low
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_module = Column(String(50), nullable=True)  # audit, rank, competitor, review, report, billing, etc.
    source_id = Column(String(255), nullable=True)  # ID of the source item
    action_label = Column(String(100), nullable=True)
    action_url = Column(String(500), nullable=True)
    is_read = Column(Boolean, default=False)
    is_acknowledged = Column(Boolean, default=False)
    is_bookmarked = Column(Boolean, default=False)
    dismissed_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    notification_date = Column(DateTime(timezone=True), nullable=False, index=True)
    metadata = Column(JSON, nullable=True)  # Additional data
    
    # Relationships
    user = relationship("User")
    app = relationship("App")
    
    __table_args__ = (
        Index('idx_notification_user_date', 'user_id', 'notification_date'),
        Index('idx_notification_unread', 'user_id', 'is_read'),
        Index('idx_notification_priority', 'user_id', 'priority'),
        Index('idx_notification_app', 'user_id', 'app_id'),
    )
