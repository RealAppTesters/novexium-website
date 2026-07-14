from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ListingVersion(BaseModel):
    __tablename__ = "listing_versions"
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey("store_listings.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    short_description = Column(String(255), nullable=True)
    long_description = Column(Text, nullable=True)
    promotional_text = Column(String(255), nullable=True)
    what_new = Column(Text, nullable=True)
    release_notes = Column(Text, nullable=True)
    version_name = Column(String(100), nullable=True)
    version_number = Column(Integer, nullable=False)
    change_summary = Column(Text, nullable=True)
    optimization_score = Column(Integer, default=0)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    is_published = Column(Boolean, default=False)
    changes = Column(JSON, nullable=True)  # Store changes made
    
    # Relationships
    listing = relationship("StoreListing", back_populates="versions")
    
    __table_args__ = (
        Index('idx_version_listing_number', 'listing_id', 'version_number'),
        Index('idx_version_published', 'listing_id', 'is_published'),
    )
