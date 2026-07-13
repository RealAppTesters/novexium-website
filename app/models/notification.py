from sqlalchemy import Column, String, Boolean, DateTime, Enum, Index, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel
import enum

class NotificationType(str, enum.Enum):
    SYSTEM = "system"
    AUDIT = "audit"
    SUBSCRIPTION = "subscription"
    REPORT = "report"
    KEYWORD = "keyword"
    REVIEW = "review"

class Notification(BaseModel):
    __tablename__ = "notifications"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    notification = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    read_status = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    __table_args__ = (
        Index('idx_notification_user_read', 'user_id', 'read_status'),
        Index('idx_notification_created', 'created_at'),
    )
