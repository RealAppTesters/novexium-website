from sqlalchemy import Column, Integer, DateTime, Float, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class KeywordRanking(BaseModel):
    __tablename__ = "keyword_rankings"
    
    app_keyword_id = Column(UUID(as_uuid=True), ForeignKey("app_keywords.id"), nullable=False, index=True)
    ranking = Column(Integer, nullable=True)
    ranking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    change = Column(Integer, nullable=True)
    
    # Relationships
    app_keyword = relationship("AppKeyword", back_populates="rankings")
    
    __table_args__ = (
        Index('idx_ranking_date_app_keyword', 'app_keyword_id', 'ranking_date'),
    )
