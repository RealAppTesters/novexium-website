from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class CompetitorSnapshot(BaseModel):
    __tablename__ = "competitor_snapshots"
    
    competitor_id = Column(UUID(as_uuid=True), ForeignKey("competitors.id"), nullable=False, index=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    visibility_score = Column(Integer, default=0)
    overall_score = Column(Integer, default=0)
    keyword_coverage = Column(Integer, default=0)
    creative_score = Column(Integer, default=0)
    store_health = Column(Integer, default=0)
    store_data = Column(JSON, nullable=True)  # Snapshot of store listing
    creative_data = Column(JSON, nullable=True)  # Snapshot of creatives
    snapshot_date = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    competitor = relationship("Competitor", back_populates="snapshots")
    
    __table_args__ = (
        Index('idx_snapshot_competitor_date', 'competitor_id', 'snapshot_date'),
    )
