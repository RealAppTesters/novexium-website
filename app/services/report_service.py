from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import json

from app.models.report import Report
from app.models.report_template import ReportTemplate
from app.models.report_schedule import ReportSchedule
from app.models.report_share import ReportShare
from app.report.builder import ReportBuilder
from app.report.export.pdf import PDFExporter
from app.report.scheduling.scheduler import ReportScheduler


class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.builder = ReportBuilder(db)
        self.exporter = PDFExporter(db)
        self.scheduler = ReportScheduler(db)
    
    def create_report(self, user_id: str, data: Dict) -> Dict:
        """Create a new report"""
        report = Report(
            id=uuid.uuid4(),
            user_id=user_id,
            app_id=data.get('app_id'),
            title=data.get('title', 'My Report'),
            description=data.get('description'),
            template_id=data.get('template_id'),
            sections=data.get('sections', []),
            settings=data.get('settings', {}),
            branding=data.get('branding', {}),
            status='draft'
        )
        
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        
        return self._report_to_dict(report)
    
    def generate_report(self, report_id: str) -> Dict:
        """Generate a report"""
        report = self.db.query(Report).filter(Report.id == report_id).first()
        if not report:
            return None
        
        # Build report data
        report_data = self.builder.build(report)
        
        # Update report
        report.data = report_data
        report.status = 'ready'
        report.generated_date = datetime.utcnow()
        self.db.commit()
        
        return self._report_to_dict(report)
    
    def export_report(self, report_id: str, format: str = 'pdf') -> Dict:
        """Export a report in specified format"""
        report = self.db.query(Report).filter(Report.id == report_id).first()
        if not report:
            return None
        
        if report.status != 'ready':
            report = self.generate_report(report_id)
        
        if format == 'pdf':
            pdf_url = self.exporter.export(report)
            report.pdf_url = pdf_url
            self.db.commit()
            return {'url': pdf_url}
        
        return {'error': f'Unsupported format: {format}'}
    
    def schedule_report(self, user_id: str, report_id: str, schedule_data: Dict) -> Dict:
        """Schedule a report"""
        schedule = ReportSchedule(
            id=uuid.uuid4(),
            user_id=user_id,
            report_id=report_id,
            frequency=schedule_data.get('frequency'),
            schedule_data=schedule_data.get('schedule_data'),
            recipients=schedule_data.get('recipients', []),
            next_run=self.scheduler.calculate_next_run(schedule_data)
        )
        
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        
        return {
            'id': str(schedule.id),
            'frequency': schedule.frequency,
            'next_run': schedule.next_run.isoformat()
        }
    
    def share_report(self, report_id: str, share_data: Dict) -> Dict:
        """Share a report via link"""
        share = ReportShare(
            id=uuid.uuid4(),
            report_id=report_id,
            share_token=str(uuid.uuid4()).replace('-', '')[:16],
            expires_at=datetime.utcnow() + timedelta(days=share_data.get('expires_in_days', 7)),
            max_views=share_data.get('max_views')
        )
        
        self.db.add(share)
        self.db.commit()
        
        return {
            'token': share.share_token,
            'expires_at': share.expires_at.isoformat(),
            'url': f'/share/report/{share.share_token}'
        }
    
    def get_reports(self, user_id: str, filters: Dict = None) -> List[Dict]:
        """Get reports for a user"""
        query = self.db.query(Report).filter(
            Report.user_id == user_id,
            Report.is_archived == False
        )
        
        if filters:
            if filters.get('app_id'):
                query = query.filter(Report.app_id == filters['app_id'])
            if filters.get('status'):
                query = query.filter(Report.status == filters['status'])
            if filters.get('favorites'):
                query = query.filter(Report.is_favorite == True)
        
        reports = query.order_by(Report.generated_date.desc()).all()
        return [self._report_to_dict(r) for r in reports]
    
    def get_templates(self, user_id: str) -> List[Dict]:
        """Get available templates"""
        templates = self.db.query(ReportTemplate).filter(
            (ReportTemplate.is_public == True) |
            (ReportTemplate.user_id == user_id)
        ).all()
        
        return [self._template_to_dict(t) for t in templates]
    
    def save_template(self, user_id: str, data: Dict) -> Dict:
        """Save a custom template"""
        template = ReportTemplate(
            id=uuid.uuid4(),
            name=data.get('name'),
            description=data.get('description'),
            sections=data.get('sections', []),
            settings=data.get('settings', {}),
            branding=data.get('branding', {}),
            is_custom=True,
            user_id=user_id
        )
        
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        
        return self._template_to_dict(template)
    
    def _report_to_dict(self, report: Report) -> Dict:
        return {
            'id': str(report.id),
            'title': report.title,
            'description': report.description,
            'status': report.status,
            'sections': report.sections,
            'settings': report.settings,
            'branding': report.branding,
            'is_favorite': report.is_favorite,
            'pdf_url': report.pdf_url,
            'generated_date': report.generated_date.isoformat() if report.generated_date else None
        }
    
    def _template_to_dict(self, template: ReportTemplate) -> Dict:
        return {
            'id': str(template.id),
            'name': template.name,
            'description': template.description,
            'category': template.category,
            'sections': template.sections,
            'settings': template.settings,
            'branding': template.branding,
            'is_system': template.is_system,
            'is_custom': template.is_custom
        }
