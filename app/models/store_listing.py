from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class StoreListing(BaseModel):
    __tablename__ = "store_listings"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True, unique=True)
    platform = Column(String(20), nullable=False)  # google_play, app_store
    title = Column(String(255), nullable=False)
    short_description = Column(String(255), nullable=True)
    long_description = Column(Text, nullable=True)
    promotional_text = Column(String(255), nullable=True)  # Google Play only
    what_new = Column(Text, nullable=True)  # App Store only
    release_notes = Column(Text, nullable=True)  # Google Play only
    language = Column(String(2), default="en")
    localization_country = Column(String(2), nullable=True)  # Country code for localization
    optimization_score = Column(Integer, default=0)
    title_score = Column(Integer, default=0)
    description_score = Column(Integer, default=0)
    readability_score = Column(Integer, default=0)
    keyword_coverage_score = Column(Integer, default=0)
    completeness_score = Column(Integer, default=0)
    last_optimized = Column(DateTime(timezone=True), nullable=True)
    is_published = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    app = relationship("App", back_populates="store_listing")
    versions = relationship("ListingVersion", back_populates="listing", cascade="all, delete-orphan")
    drafts = relationship("ListingDraft", back_populates="listing", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_listing_app_platform', 'app_id', 'platform'),
        Index('idx_listing_language', 'app_id', 'language'),
        Index('idx_listing_optimization', 'optimization_score'),
    )
