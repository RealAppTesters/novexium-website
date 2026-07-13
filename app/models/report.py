from sqlalchemy import Column, String, DateTime, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel
import enum

class ReportType(str, enum.Enum):
    ASO_AUDIT = "aso_audit"
    KEYWORD_TRACKING = "keyword_tracking"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    PERFORMANCE_REPORT = "performance_report"

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Report(BaseModel):
    __tablename__ = "reports"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id"), nullable=True, index=True)
    pdf_file = Column(String(500), nullable=True)  # URL to PDF
    report_type = Column(Enum(ReportType), nullable=False)
    generated_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    app = relationship("App", back_populates="reports")
    
    __table_args__ = (
        Index('idx_report_user_date', 'user_id', 'generated_date'),
        Index('idx_report_status', 'status'),
    )
