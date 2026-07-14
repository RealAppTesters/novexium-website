from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class Keyword(BaseModel):
    __tablename__ = "keywords"
    
    keyword = Column(String(255), nullable=False, index=True)
    search_volume = Column(Integer, nullable=True)
    difficulty = Column(Integer, nullable=True)  # 0-100
    opportunity_score = Column(Integer, nullable=True)  # 0-100
    estimated_traffic = Column(Integer, nullable=True)
    competition = Column(String(20), nullable=True)  # low, medium, high
    country = Column(String(2), nullable=True)
    language = Column(String(2), nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    category = Column(String(100), nullable=True)  # auto-detected category
    is_trending = Column(Boolean, default=False)
    trend_direction = Column(String(10), nullable=True)  # up, down, stable
    
    # Relationships
    app_keywords = relationship("AppKeyword", back_populates="keyword")
    
    __table_args__ = (
        Index('idx_keyword_country_lang', 'keyword', 'country', 'language'),
        Index('idx_keyword_opportunity', 'opportunity_score'),
        Index('idx_keyword_trending', 'is_trending'),
    )
