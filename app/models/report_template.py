from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class ReportTemplate(BaseModel):
    __tablename__ = "report_templates"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # executive, weekly, monthly, quarterly, agency, audit
    sections = Column(JSON, nullable=False)  # Default sections
    settings = Column(JSON, nullable=True)  # Default settings
    branding = Column(JSON, nullable=True)  # Default branding
    is_system = Column(Boolean, default=False)
    is_custom = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    usage_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User")
    reports = relationship("Report", back_populates="template")
    
    __table_args__ = (
        Index('idx_template_category', 'category'),
        Index('idx_template_user', 'user_id'),
        Index('idx_template_public', 'is_public'),
    )
