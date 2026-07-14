from sqlalchemy import Column, Integer, DateTime, Float, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class AppKeyword(BaseModel):
    __tablename__ = "app_keywords"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"), nullable=False, index=True)
    current_ranking = Column(Integer, nullable=True)
    previous_ranking = Column(Integer, nullable=True)
    best_ranking = Column(Integer, nullable=True)
    worst_ranking = Column(Integer, nullable=True)
    ranking_change = Column(Integer, nullable=True)  # Positive = improvement
    ranking_date = Column(DateTime(timezone=True), nullable=False)
    is_tracked = Column(Boolean, default=True)
    
    # Relationships
    app = relationship("App", back_populates="app_keywords")
    keyword = relationship("Keyword", back_populates="app_keywords")
    
    __table_args__ = (
        Index('idx_app_keyword_date', 'app_id', 'keyword_id', 'ranking_date'),
        Index('idx_app_keyword_ranking', 'app_id', 'current_ranking'),
        Index('idx_app_keyword_tracked', 'app_id', 'is_tracked'),
    )
