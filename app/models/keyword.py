from sqlalchemy import Column, String, Integer, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Keyword(BaseModel):
    __tablename__ = "keywords"
    
    keyword = Column(String(255), nullable=False, index=True)
    search_volume = Column(Integer, nullable=True)
    difficulty = Column(Integer, nullable=True)  # 0-100
    opportunity_score = Column(Float, nullable=True)  # 0-100
    ranking = Column(Integer, nullable=True)
    estimated_traffic = Column(Integer, nullable=True)
    country = Column(String(2), nullable=True)  # ISO country code
    language = Column(String(2), nullable=True)  # ISO language code
    last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    app_keywords = relationship("AppKeyword", back_populates="keyword")
    
    __table_args__ = (
        Index('idx_keyword_country_lang', 'keyword', 'country', 'language'),
        Index('idx_keyword_search_volume', 'search_volume'),
        Index('idx_keyword_opportunity', 'opportunity_score'),
    )
