from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class CreativeAnalysis(BaseModel):
    __tablename__ = "creative_analyses"
    
    asset_id = Column(UUID(as_uuid=True), ForeignKey("creative_assets.id"), nullable=False, index=True)
    analysis_type = Column(String(50), nullable=False)  # icon, screenshot, feature_graphic, video
    score = Column(Integer, default=0)
    findings = Column(JSON, nullable=True)  # List of findings
    recommendations = Column(JSON, nullable=True)  # Recommendations
    metrics = Column(JSON, nullable=True)  # Detailed metrics
    analysis_date = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    asset = relationship("CreativeAsset", back_populates="analysis")
    
    __table_args__ = (
        Index('idx_analysis_asset_date', 'asset_id', 'analysis_date'),
    )
