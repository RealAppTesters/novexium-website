from sqlalchemy import Column, String, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class KeywordGroup(BaseModel):
    __tablename__ = "keyword_groups"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    keywords = Column(JSON, nullable=True)  # List of keyword IDs
    is_custom = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    color = Column(String(7), nullable=True)  # Hex color
    
    __table_args__ = (
        Index('idx_group_app', 'app_id'),
        Index('idx_group_pinned', 'app_id', 'is_pinned'),
    )
