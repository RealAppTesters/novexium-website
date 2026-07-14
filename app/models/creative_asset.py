from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class CreativeAsset(BaseModel):
    __tablename__ = "creative_assets"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    asset_type = Column(String(50), nullable=False)  # icon, screenshot, feature_graphic, video, banner
    asset_url = Column(String(500), nullable=True)
    asset_hash = Column(String(64), nullable=True)  # For change detection
    filename = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)  # In bytes
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    aspect_ratio = Column(Float, nullable=True)
    format = Column(String(20), nullable=True)  # png, jpg, mp4, etc.
    order = Column(Integer, nullable=True)  # For screenshot order
    is_published = Column(Boolean, default=True)
    is_primary = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    analysis_score = Column(Integer, default=0)
    analysis_data = Column(JSON, nullable=True)  # Detailed analysis results
    last_analyzed = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    app = relationship("App", back_populates="creative_assets")
    analysis = relationship("CreativeAnalysis", back_populates="asset", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_asset_app_type', 'app_id', 'asset_type'),
        Index('idx_asset_published', 'app_id', 'is_published'),
        Index('idx_asset_hash', 'asset_hash'),
    )
