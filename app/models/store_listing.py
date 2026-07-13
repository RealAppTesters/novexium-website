from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel

class StoreListing(BaseModel):
    __tablename__ = "store_listings"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True, unique=True)
    title = Column(String(255), nullable=False)
    short_description = Column(String(255), nullable=True)
    long_description = Column(Text, nullable=True)
    release_notes = Column(Text, nullable=True)
    character_count = Column(Integer, nullable=True)
    optimization_score = Column(Float, nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    app = relationship("App", back_populates="store_listing")
