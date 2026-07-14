from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ListingDraft(BaseModel):
    __tablename__ = "listing_drafts"
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey("store_listings.id"), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    short_description = Column(String(255), nullable=True)
    long_description = Column(Text, nullable=True)
    promotional_text = Column(String(255), nullable=True)
    what_new = Column(Text, nullable=True)
    release_notes = Column(Text, nullable=True)
    draft_name = Column(String(100), nullable=True)
    optimization_score = Column(Integer, default=0)
    last_autosave = Column(DateTime(timezone=True), nullable=True)
    changes = Column(JSON, nullable=True)
    is_autosave = Column(Boolean, default=False)
    
    # Relationships
    listing = relationship("StoreListing", back_populates="drafts")
    
    __table_args__ = (
        Index('idx_draft_listing', 'listing_id'),
        Index('idx_draft_autosave', 'listing_id', 'is_autosave'),
    )
