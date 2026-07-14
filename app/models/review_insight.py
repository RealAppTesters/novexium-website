from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ReviewInsight(BaseModel):
    __tablename__ = "review_insights"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    insight_type = Column(String(50), nullable=False)  # trend, issue, opportunity, feature_request
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    impact = Column(String(20), nullable=True)  # high, medium, low
    supporting_reviews = Column(JSON, nullable=True)  # List of review IDs
    supporting_count = Column(Integer, default=0)
    sentiment = Column(String(20), nullable=True)
    recommendation = Column(Text, nullable=True)
    is_acknowledged = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    detected_date = Column(DateTime(timezone=True), nullable=False)
    
    __table_args__ = (
        Index('idx_insight_app_type', 'app_id', 'insight_type'),
        Index('idx_insight_impact', 'app_id', 'impact'),
    )
