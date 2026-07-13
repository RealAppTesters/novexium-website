from sqlalchemy import Column, String, Text, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel

class ActivityLog(BaseModel):
    __tablename__ = "activity_logs"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    details = Column(JSON, nullable=True)  # Store as JSON
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs")
    
    __table_args__ = (
        Index('idx_activity_user_action', 'user_id', 'action'),
        Index('idx_activity_created', 'created_at'),
        Index('idx_activity_action_date', 'action', 'created_at'),
    )
