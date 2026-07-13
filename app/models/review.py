from sqlalchemy import Column, String, Integer, Float, Boolean, Text, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel
import enum

class Sentiment(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class ReplyStatus(str, enum.Enum):
    PENDING = "pending"
    REPLIED = "replied"
    SKIPPED = "skipped"

class Review(BaseModel):
    __tablename__ = "reviews"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    reviewer = Column(String(255), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255), nullable=True)
    review = Column(Text, nullable=True)
    sentiment = Column(Enum(Sentiment), nullable=True)
    category = Column(String(100), nullable=True)
    language = Column(String(2), nullable=True)  # ISO language code
    reply_status = Column(Enum(ReplyStatus), default=ReplyStatus.PENDING)
    
    # Relationships
    app = relationship("App", back_populates="reviews")
    
    __table_args__ = (
        Index('idx_review_app_rating', 'app_id', 'rating'),
        Index('idx_review_sentiment', 'sentiment'),
        Index('idx_review_created', 'created_at'),
        Index('idx_review_reply_status', 'reply_status'),
    )
