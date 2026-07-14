from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class VisibilityRecord(BaseModel):
    __tablename__ = "visibility_records"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    country = Column(String(2), nullable=False)
    language = Column(String(2), nullable=False)
    platform = Column(String(20), nullable=False)
    visibility_score = Column(Float, default=0)
    previous_visibility = Column(Float, default=0)
    visibility_change = Column(Float, default=0)
    tracked_keywords = Column(Integer, default=0)
    top_3_count = Column(Integer, default=0)
    top_10_count = Column(Integer, default=0)
    top_25_count = Column(Integer, default=0)
    top_50_count = Column(Integer, default=0)
    organic_reach_estimate = Column(Integer, default=0)
    record_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    __table_args__ = (
        Index('idx_visibility_app_date', 'app_id', 'record_date'),
        Index('idx_visibility_app_country', 'app_id', 'country'),
    )
