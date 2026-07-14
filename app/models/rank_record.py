from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class RankRecord(BaseModel):
    __tablename__ = "rank_records"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"), nullable=False, index=True)
    keyword = Column(String(255), nullable=False)
    country = Column(String(2), nullable=False)
    language = Column(String(2), nullable=False)
    platform = Column(String(20), nullable=False)  # app_store, google_play
    current_position = Column(Integer, nullable=True)
    previous_position = Column(Integer, nullable=True)
    best_position = Column(Integer, nullable=True)
    worst_position = Column(Integer, nullable=True)
    position_change = Column(Integer, nullable=True)  # Positive = improvement
    visibility_score = Column(Float, default=0)
    search_volume = Column(Integer, nullable=True)
    rank_date = Column(DateTime(timezone=True), nullable=False, index=True)
    is_tracked = Column(Boolean, default=True)
    is_favorite = Column(Boolean, default=False)
    category = Column(String(100), nullable=True)  # keyword category
    
    __table_args__ = (
        Index('idx_rank_app_keyword_date', 'app_id', 'keyword_id', 'rank_date'),
        Index('idx_rank_app_country', 'app_id', 'country'),
        Index('idx_rank_app_position', 'app_id', 'current_position'),
        Index('idx_rank_change', 'app_id', 'position_change'),
    )
