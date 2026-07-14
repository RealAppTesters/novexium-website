from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class Competitor(BaseModel):
    __tablename__ = "competitors"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    competitor_app_id = Column(String(255), nullable=False)  # Store app ID or package name
    competitor_name = Column(String(255), nullable=False)
    platform = Column(String(20), nullable=False)  # app_store, google_play
    store_url = Column(String(500), nullable=True)
    developer = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    country = Column(String(2), nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    visibility_score = Column(Integer, default=0)
    overall_score = Column(Integer, default=0)
    keyword_coverage = Column(Integer, default=0)
    creative_score = Column(Integer, default=0)
    store_health = Column(Integer, default=0)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    is_pinned = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    discovery_method = Column(String(50), nullable=True)  # category, keyword, manual, store
    discovery_confidence = Column(Integer, nullable=True)  # 0-100
    
    # Relationships
    app = relationship("App", back_populates="competitors")
    snapshots = relationship("CompetitorSnapshot", back_populates="competitor", cascade="all, delete-orphan")
    changes = relationship("CompetitorChange", back_populates="competitor", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_competitor_app', 'app_id'),
        Index('idx_competitor_pinned', 'app_id', 'is_pinned'),
        Index('idx_competitor_active', 'app_id', 'is_active'),
        Index('idx_competitor_platform', 'platform'),
    )
