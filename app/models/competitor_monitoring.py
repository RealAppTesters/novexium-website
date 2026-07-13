from sqlalchemy import Column, JSON, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel

class CompetitorMonitoring(BaseModel):
    __tablename__ = "competitor_monitoring"
    
    competitor_id = Column(UUID(as_uuid=True), ForeignKey("competitors.id"), nullable=False, index=True)
    keywords = Column(JSON, nullable=True)  # Store as JSON array
    ratings = Column(JSON, nullable=True)   # Store as JSON object
    screenshots = Column(JSON, nullable=True)  # Store as JSON array
    store_listing = Column(JSON, nullable=True)  # Store as JSON object
    visibility = Column(JSON, nullable=True)  # Store as JSON object
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Relationships
    competitor = relationship("Competitor", back_populates="monitoring")
    
    __table_args__ = (
        Index('idx_monitoring_competitor_date', 'competitor_id', 'date'),
    )
