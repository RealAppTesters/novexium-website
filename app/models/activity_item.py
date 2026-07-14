from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ActivityItem(BaseModel):
    __tablename__ = "activity_items"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=True, index=True)
    activity_type = Column(String(50), nullable=False)  # app_connected, audit_completed, rank_changed, etc.
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_module = Column(String(50), nullable=True)
    source_id = Column(String(255), nullable=True)
    activity_date = Column(DateTime(timezone=True), nullable=False, index=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User")
    app = relationship("App")
    
    __table_args__ = (
        Index('idx_activity_user_date', 'user_id', 'activity_date'),
        Index('idx_activity_app', 'user_id', 'app_id'),
        Index('idx_activity_type', 'activity_type'),
    )
