from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class Audit(BaseModel):
    __tablename__ = "audits"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    overall_score = Column(Integer, nullable=False)
    metadata_score = Column(Integer, nullable=False)
    keyword_score = Column(Integer, nullable=False)
    creative_score = Column(Integer, nullable=False)
    review_score = Column(Integer, nullable=False)
    competitor_score = Column(Integer, nullable=False)
    store_health_score = Column(Integer, nullable=False)
    findings = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    next_win = Column(JSON, nullable=True)
    quick_wins = Column(JSON, nullable=True)
    audit_date = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    app = relationship("App", back_populates="audits")
    user = relationship("User", back_populates="audits")
