from sqlalchemy import Column, Float, Text, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel

class Audit(BaseModel):
    __tablename__ = "audits"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=False, index=True)
    overall_score = Column(Float, nullable=False)
    keyword_score = Column(Float, nullable=False)
    metadata_score = Column(Float, nullable=False)
    creative_score = Column(Float, nullable=False)
    review_score = Column(Float, nullable=False)
    recommendations = Column(JSON, nullable=True)  # Store as JSON array
    audit_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Relationships
    app = relationship("App", back_populates="audits")
    
    __table_args__ = (
        Index('idx_audit_app_date', 'app_id', 'audit_date'),
        Index('idx_audit_overall_score', 'overall_score'),
    )
