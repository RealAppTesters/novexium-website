from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class CompetitorChange(BaseModel):
    __tablename__ = "competitor_changes"
    
    competitor_id = Column(UUID(as_uuid=True), ForeignKey("competitors.id"), nullable=False, index=True)
    change_type = Column(String(50), nullable=False)  # listing, creative, rating, review, keyword, version
    change_description = Column(Text, nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    impact = Column(String(20), nullable=True)  # high, medium, low
    impact_score = Column(Integer, nullable=True)  # 0-100
    detected_date = Column(DateTime(timezone=True), nullable=False)
    is_processed = Column(Boolean, default=False)
    
    # Relationships
    competitor = relationship("Competitor", back_populates="changes")
    
    __table_args__ = (
        Index('idx_change_competitor_date', 'competitor_id', 'detected_date'),
        Index('idx_change_processed', 'is_processed'),
    )
