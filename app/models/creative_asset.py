from sqlalchemy import Column, String, JSON, DateTime, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel
import enum

class AssetType(str, enum.Enum):
    SCREENSHOT = "screenshot"
    FEATURE_GRAPHIC = "feature_graphic"
    APP_ICON = "app_icon"
    PROMO_VIDEO = "promo_video"

class CreativeAsset(BaseModel):
    __tablename__ = "creative_assets"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    asset_url = Column(String(500), nullable=False)  # URL to asset
    analysis_results = Column(JSON, nullable=True)  # Store analysis as JSON
    upload_date = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    app = relationship("App", back_populates="creative_assets")
    
    __table_args__ = (
        Index('idx_asset_app_type', 'app_id', 'asset_type'),
    )
