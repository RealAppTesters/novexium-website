from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel


class Report(BaseModel):
    __tablename__ = "reports"
    
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("report_templates.id"), nullable=True)
    sections = Column(JSON, nullable=True)  # Ordered list of sections
    settings = Column(JSON, nullable=True)  # Report settings
    branding = Column(JSON, nullable=True)  # Branding settings
    data = Column(JSON, nullable=True)  # Cached report data
    pdf_url = Column(String(500), nullable=True)
    status = Column(String(20), default="draft")  # draft, generating, ready, failed
    is_favorite = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    generated_date = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    app = relationship("App", back_populates="reports")
    user = relationship("User", back_populates="reports")
    template = relationship("ReportTemplate", back_populates="reports")
    
    __table_args__ = (
        Index('idx_report_user_date', 'user_id', 'generated_date'),
        Index('idx_report_status', 'status'),
        Index('idx_report_app', 'app_id'),
    )
