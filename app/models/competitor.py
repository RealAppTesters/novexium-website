from sqlalchemy import Column, String, Float, Integer, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel

class Competitor(BaseModel):
    __tablename__ = "competitors"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    competitor_app = Column(String(255), nullable=False)
    store_url = Column(String(500), nullable=False)
    rating = Column(Float, nullable=True)
    reviews = Column(Integer, nullable=True)
    estimated_downloads = Column(Integer, nullable=True)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    country = Column(String(2), nullable=True)
    
    # Relationships
    app = relationship("App", back_populates="competitors")
    monitoring = relationship("CompetitorMonitoring", back_populates="competitor", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_competitor_app_url', 'app_id', 'store_url'),
        Index('idx_competitor_last_checked', 'last_checked'),
    )
