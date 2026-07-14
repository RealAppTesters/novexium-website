from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class RankAlert(BaseModel):
    __tablename__ = "rank_alerts"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"), nullable=True)
    keyword = Column(String(255), nullable=True)
    country = Column(String(2), nullable=True)
    alert_type = Column(String(50), nullable=False)  # top_10, top_3, drop, improvement, visibility
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    previous_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    severity = Column(String(20), nullable=True)  # high, medium, low
    is_read = Column(Boolean, default=False)
    is_acknowledged = Column(Boolean, default=False)
    alert_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    __table_args__ = (
        Index('idx_alert_app_date', 'app_id', 'alert_date'),
        Index('idx_alert_unread', 'app_id', 'is_read'),
    )
