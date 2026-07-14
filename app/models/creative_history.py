from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class CreativeHistory(BaseModel):
    __tablename__ = "creative_histories"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("creative_assets.id"), nullable=True)
    asset_type = Column(String(50), nullable=False)
    change_type = Column(String(50), nullable=False)  # added, removed, modified, replaced
    old_url = Column(String(500), nullable=True)
    new_url = Column(String(500), nullable=True)
    old_hash = Column(String(64), nullable=True)
    new_hash = Column(String(64), nullable=True)
    old_score = Column(Integer, nullable=True)
    new_score = Column(Integer, nullable=True)
    change_summary = Column(Text, nullable=True)
    detected_date = Column(DateTime(timezone=True), nullable=False)
    
    __table_args__ = (
        Index('idx_history_app_type', 'app_id', 'asset_type'),
        Index('idx_history_detected', 'detected_date'),
    )
