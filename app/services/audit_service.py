from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.audit.engine import AuditEngine
from app.models.audit import Audit
from app.models.app import App


class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.engine = AuditEngine(db)
    
    def run_audit(self, app_id: str, user_id: str) -> Dict[str, Any]:
        """Run a new audit for an app"""
        return self.engine.run_audit(app_id, user_id)
    
    def get_audit(self, audit_id: str) -> Optional[Dict]:
        """Get a specific audit by ID"""
        audit = self.db.query(Audit).filter(Audit.id == audit_id).first()
        if not audit:
            return None
        
        return {
            'id': str(audit.id),
            'app_id': str(audit.app_id),
            'overall_score': audit.overall_score,
            'scores': {
                'metadata': audit.metadata_score,
                'keywords': audit.keyword_score,
                'creatives': audit.creative_score,
                'reviews': audit.review_score,
                'competitors': audit.competitor_score,
                'store_health': audit.store_health_score
            },
            'findings': audit.findings,
            'recommendations': audit.recommendations,
            'next_win': audit.next_win,
            'quick_wins': audit.quick_wins,
            'audit_date': audit.audit_date.isoformat()
        }
    
    def get_audit_history(self, app_id: str) -> List[Dict]:
        """Get audit history for an app"""
        audits = self.db.query(Audit).filter(
            Audit.app_id == app_id
        ).order_by(Audit.audit_date.desc()).all()
        
        return [{
            'id': str(a.id),
            'overall_score': a.overall_score,
            'audit_date': a.audit_date.isoformat()
        } for a in audits]
    
    def compare_audits(self, audit_id1: str, audit_id2: str) -> Dict:
        """Compare two audits"""
        audit1 = self.db.query(Audit).filter(Audit.id == audit_id1).first()
        audit2 = self.db.query(Audit).filter(Audit.id == audit_id2).first()
        
        if not audit1 or not audit2:
            return None
        
        return {
            'scores': {
                'audit1': {
                    'overall': audit1.overall_score,
                    'metadata': audit1.metadata_score,
                    'keywords': audit1.keyword_score,
                    'creatives': audit1.creative_score,
                    'reviews': audit1.review_score,
                    'competitors': audit1.competitor_score,
                    'store_health': audit1.store_health_score
                },
                'audit2': {
                    'overall': audit2.overall_score,
                    'metadata': audit2.metadata_score,
                    'keywords': audit2.keyword_score,
                    'creatives': audit2.creative_score,
                    'reviews': audit2.review_score,
                    'competitors': audit2.competitor_score,
                    'store_health': audit2.store_health_score
                },
                'changes': {
                    'overall': audit2.overall_score - audit1.overall_score,
                    'metadata': audit2.metadata_score - audit1.metadata_score,
                    'keywords': audit2.keyword_score - audit1.keyword_score,
                    'creatives': audit2.creative_score - audit1.creative_score,
                    'reviews': audit2.review_score - audit1.review_score,
                    'competitors': audit2.competitor_score - audit1.competitor_score,
                    'store_health': audit2.store_health_score - audit1.store_health_score
                }
            },
            'date1': audit1.audit_date.isoformat(),
            'date2': audit2.audit_date.isoformat()
        }
