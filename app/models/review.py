from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    review_id = Column(String(255), nullable=False, unique=True)  # Store review ID
    reviewer = Column(String(255), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    theme = Column(String(100), nullable=True)  # Primary theme
    categories = Column(JSON, nullable=True)  # Multiple categories
    language = Column(String(2), nullable=True)
    country = Column(String(2), nullable=True)
    version = Column(String(50), nullable=True)
    review_date = Column(DateTime(timezone=True), nullable=False, index=True)
    is_responded = Column(Boolean, default=False)
    response = Column(Text, nullable=True)
    response_date = Column(DateTime(timezone=True), nullable=True)
    is_bookmarked = Column(Boolean, default=False)
    is_processed = Column(Boolean, default=False)
    
    # Relationships
    app = relationship("App", back_populates="reviews")
    
    __table_args__ = (
        Index('idx_review_app_date', 'app_id', 'review_date'),
        Index('idx_review_sentiment', 'app_id', 'sentiment'),
        Index('idx_review_theme', 'app_id', 'theme'),
        Index('idx_review_rating', 'app_id', 'rating'),
    )
