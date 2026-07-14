from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.models.competitor import Competitor
from app.models.competitor_snapshot import CompetitorSnapshot
from app.models.competitor_change import CompetitorChange
from app.competitor.discovery.category import CategoryDiscovery
from app.competitor.comparison.benchmark import BenchmarkEngine
from app.competitor.insights.generator import InsightGenerator
from app.competitor.alerts.alert_service import AlertService


class CompetitorService:
    def __init__(self, db: Session):
        self.db = db
        self.discovery = CategoryDiscovery()
        self.benchmark_engine = BenchmarkEngine()
        self.insight_generator = InsightGenerator()
        self.alert_service = AlertService(db)
    
    def discover_competitors(self, app_id: str, app_data: Dict) -> List[Dict]:
        """Discover competitors for an app"""
        candidates = self.discovery.discover(app_data)
        
        saved = []
        for candidate in candidates:
            # Check if already exists
            existing = self.db.query(Competitor).filter(
                Competitor.app_id == app_id,
                Competitor.competitor_name == candidate['name']
            ).first()
            
            if not existing:
                competitor = Competitor(
                    id=uuid.uuid4(),
                    app_id=app_id,
                    competitor_app_id=candidate.get('app_id', ''),
                    competitor_name=candidate['name'],
                    platform=app_data.get('platform', 'app_store'),
                    developer=candidate.get('developer'),
                    category=candidate.get('category'),
                    country=app_data.get('country'),
                    rating=candidate.get('rating'),
                    review_count=candidate.get('review_count'),
                    discovery_method='category',
                    discovery_confidence=candidate.get('confidence', 50),
                    last_checked=datetime.utcnow(),
                    is_active=True
                )
                self.db.add(competitor)
                saved.append(competitor)
        
        self.db.commit()
        
        return [self._competitor_to_dict(c) for c in saved]
    
    def get_competitors(self, app_id: str) -> List[Dict]:
        """Get all competitors for an app"""
        competitors = self.db.query(Competitor).filter(
            Competitor.app_id == app_id,
            Competitor.is_active == True
        ).order_by(Competitor.is_pinned.desc(), Competitor.overall_score.desc()).all()
        
        return [self._competitor_to_dict(c) for c in competitors]
    
    def get_competitor_detail(self, competitor_id: str) -> Dict:
        """Get detailed competitor profile"""
        competitor = self.db.query(Competitor).filter(
            Competitor.id == competitor_id
        ).first()
        
        if not competitor:
            return None
        
        snapshots = self.db.query(CompetitorSnapshot).filter(
            CompetitorSnapshot.competitor_id == competitor_id
        ).order_by(CompetitorSnapshot.snapshot_date.desc()).limit(10).all()
        
        changes = self.db.query(CompetitorChange).filter(
            CompetitorChange.competitor_id == competitor_id
        ).order_by(CompetitorChange.detected_date.desc()).limit(20).all()
        
        return {
            'competitor': self._competitor_to_dict(competitor),
            'snapshots': [self._snapshot_to_dict(s) for s in snapshots],
            'changes': [self._change_to_dict(c) for c in changes]
        }
    
    def compare_competitors(self, app_id: str, competitor_ids: List[str]) -> Dict:
        """Compare app against selected competitors"""
        # Get app data
        app = self.db.query(App).filter(App.id == app_id).first()
        
        # Get competitors
        competitors = self.db.query(Competitor).filter(
            Competitor.id.in_(competitor_ids)
        ).all()
        
        app_data = {
            'name': app.app_name,
            'growth_score': 87,
            'visibility_score': 92,
            'rating': 4.8,
            'review_count': 247,
            'keyword_coverage': 78,
            'creative_score': 71,
            'store_health': 82,
            'update_frequency': 75
        }
        
        competitor_data = [self._competitor_to_benchmark_data(c) for c in competitors]
        
        return self.benchmark_engine.compare(app_data, competitor_data)
    
    def get_changes(self, app_id: str, days: int = 7) -> List[Dict]:
        """Get recent competitor changes"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        changes = self.db.query(CompetitorChange).join(
            Competitor
        ).filter(
            Competitor.app_id == app_id,
            CompetitorChange.detected_date >= cutoff
        ).order_by(CompetitorChange.detected_date.desc()).limit(50).all()
        
        return [self._change_to_dict(c) for c in changes]
    
    def get_insights(self, app_id: str) -> List[Dict]:
        """Get competitor insights"""
        changes = self.get_changes(app_id, 14)
        competitors = self.get_competitors(app_id)
        
        return self.insight_generator.generate(changes, competitors)
    
    def pin_competitor(self, competitor_id: str) -> Dict:
        """Pin a competitor to watchlist"""
        competitor = self.db.query(Competitor).filter(Competitor.id == competitor_id).first()
        if competitor:
            competitor.is_pinned = not competitor.is_pinned
            self.db.commit()
            return {'pinned': competitor.is_pinned}
        return {'error': 'Competitor not found'}
    
    def remove_competitor(self, competitor_id: str) -> Dict:
        """Remove a competitor"""
        competitor = self.db.query(Competitor).filter(Competitor.id == competitor_id).first()
        if competitor:
            competitor.is_active = False
            self.db.commit()
            return {'removed': True}
        return {'error': 'Competitor not found'}
    
    def _competitor_to_dict(self, competitor: Competitor) -> Dict:
        return {
            'id': str(competitor.id),
            'name': competitor.competitor_name,
            'developer': competitor.developer,
            'platform': competitor.platform,
            'category': competitor.category,
            'rating': competitor.rating,
            'review_count': competitor.review_count,
            'overall_score': competitor.overall_score,
            'visibility_score': competitor.visibility_score,
            'is_pinned': competitor.is_pinned,
            'last_checked': competitor.last_checked.isoformat() if competitor.last_checked else None,
            'discovery_confidence': competitor.discovery_confidence
        }
    
    def _snapshot_to_dict(self, snapshot: CompetitorSnapshot) -> Dict:
        return {
            'id': str(snapshot.id),
            'rating': snapshot.rating,
            'review_count': snapshot.review_count,
            'visibility_score': snapshot.visibility_score,
            'overall_score': snapshot.overall_score,
            'snapshot_date': snapshot.snapshot_date.isoformat()
        }
    
    def _change_to_dict(self, change: CompetitorChange) -> Dict:
        return {
            'id': str(change.id),
            'type': change.change_type,
            'description': change.change_description,
            'impact': change.impact,
            'detected_date': change.detected_date.isoformat()
        }
    
    def _competitor_to_benchmark_data(self, competitor: Competitor) -> Dict:
        return {
            'name': competitor.competitor_name,
            'rating': competitor.rating or 0,
            'review_count': competitor.review_count or 0,
            'visibility_score': competitor.visibility_score or 0,
            'keyword_coverage': competitor.keyword_coverage or 0,
            'creative_score': competitor.creative_score or 0,
            'store_health': competitor.store_health or 0,
            'growth_score': competitor.overall_score or 0,
            'update_frequency': 50  # Default
        }
