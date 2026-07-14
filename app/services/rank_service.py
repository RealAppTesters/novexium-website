from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
import uuid
import random

from app.models.rank_record import RankRecord
from app.models.visibility_record import VisibilityRecord
from app.models.rank_alert import RankAlert
from app.rank.tracking.app_store import AppStoreRankTracker
from app.rank.tracking.google_play import GooglePlayRankTracker
from app.rank.visibility.scorer import VisibilityScorer
from app.rank.visibility.trends import TrendAnalyzer
from app.rank.alerts.alert_service import AlertService


class RankService:
    def __init__(self, db: Session):
        self.db = db
        self.trackers = {
            'app_store': AppStoreRankTracker(),
            'google_play': GooglePlayRankTracker()
        }
        self.visibility_scorer = VisibilityScorer()
        self.trend_analyzer = TrendAnalyzer()
        self.alert_service = AlertService(db)
    
    def update_rankings(self, app_id: str, platform: str, 
                        keywords: List[str], country: str = 'US',
                        language: str = 'en') -> Dict[str, Any]:
        """Update rankings for keywords"""
        tracker = self.trackers.get(platform)
        if not tracker:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Fetch rankings
        rankings = tracker.get_rankings(app_id, keywords, country, language)
        
        saved = []
        for rank_data in rankings:
            # Get existing record
            existing = self.db.query(RankRecord).filter(
                RankRecord.app_id == app_id,
                RankRecord.keyword == rank_data['keyword'],
                RankRecord.country == country,
                RankRecord.language == language
            ).order_by(RankRecord.rank_date.desc()).first()
            
            previous_position = existing.current_position if existing else None
            
            # Calculate change
            position_change = None
            if previous_position and rank_data['position']:
                position_change = previous_position - rank_data['position']
            
            # Create record
            record = RankRecord(
                id=uuid.uuid4(),
                app_id=app_id,
                keyword_id=rank_data.get('keyword_id'),
                keyword=rank_data['keyword'],
                country=country,
                language=language,
                platform=platform,
                current_position=rank_data['position'],
                previous_position=previous_position,
                position_change=position_change,
                visibility_score=self.visibility_scorer.calculate_score(rank_data['position']),
                search_volume=rank_data.get('search_volume'),
                rank_date=datetime.utcnow()
            )
            
            self.db.add(record)
            saved.append(record)
            
            # Check for alerts
            if position_change and abs(position_change) >= 5:
                self.alert_service.create_rank_alert(
                    app_id, rank_data['keyword'], country,
                    position_change, previous_position, rank_data['position']
                )
        
        self.db.commit()
        
        # Update visibility record
        self._update_visibility_record(app_id, country, language, platform)
        
        return {
            'total': len(saved),
            'keywords': [r.keyword for r in saved],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_rankings(self, app_id: str, country: str = 'US', 
                     language: str = 'en', limit: int = 100) -> List[Dict]:
        """Get current rankings"""
        # Get latest rank date
        latest = self.db.query(func.max(RankRecord.rank_date)).filter(
            RankRecord.app_id == app_id,
            RankRecord.country == country,
            RankRecord.language == language
        ).scalar()
        
        if not latest:
            return []
        
        records = self.db.query(RankRecord).filter(
            RankRecord.app_id == app_id,
            RankRecord.country == country,
            RankRecord.language == language,
            RankRecord.rank_date == latest,
            RankRecord.is_tracked == True
        ).order_by(RankRecord.current_position).limit(limit).all()
        
        return [self._rank_record_to_dict(r) for r in records]
    
    def get_visibility(self, app_id: str, country: str = 'US',
                       language: str = 'en') -> Dict[str, Any]:
        """Get visibility data"""
        latest = self.db.query(func.max(VisibilityRecord.record_date)).filter(
            VisibilityRecord.app_id == app_id,
            VisibilityRecord.country == country,
            VisibilityRecord.language == language
        ).scalar()
        
        if not latest:
            return self._get_empty_visibility()
        
        record = self.db.query(VisibilityRecord).filter(
            VisibilityRecord.app_id == app_id,
            VisibilityRecord.country == country,
            VisibilityRecord.language == language,
            VisibilityRecord.record_date == latest
        ).first()
        
        if not record:
            return self._get_empty_visibility()
        
        return {
            'visibility_score': record.visibility_score,
            'previous_visibility': record.previous_visibility,
            'visibility_change': record.visibility_change,
            'tracked_keywords': record.tracked_keywords,
            'top_3_count': record.top_3_count,
            'top_10_count': record.top_10_count,
            'top_25_count': record.top_25_count,
            'top_50_count': record.top_50_count,
            'organic_reach_estimate': record.organic_reach_estimate,
            'record_date': record.record_date.isoformat()
        }
    
    def get_rank_history(self, app_id: str, keyword: str, country: str = 'US',
                         language: str = 'en', days: int = 30) -> List[Dict]:
        """Get rank history for a keyword"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        records = self.db.query(RankRecord).filter(
            RankRecord.app_id == app_id,
            RankRecord.keyword == keyword,
            RankRecord.country == country,
            RankRecord.language == language,
            RankRecord.rank_date >= cutoff
        ).order_by(RankRecord.rank_date.asc()).all()
        
        return [{
            'position': r.current_position,
            'date': r.rank_date.isoformat()
        } for r in records]
    
    def get_alerts(self, app_id: str, limit: int = 20) -> List[Dict]:
        """Get rank alerts"""
        alerts = self.db.query(RankAlert).filter(
            RankAlert.app_id == app_id
        ).order_by(RankAlert.alert_date.desc()).limit(limit).all()
        
        return [self._alert_to_dict(a) for a in alerts]
    
    def acknowledge_alert(self, alert_id: str) -> Dict:
        """Acknowledge an alert"""
        alert = self.db.query(RankAlert).filter(RankAlert.id == alert_id).first()
        if alert:
            alert.is_acknowledged = True
            alert.is_read = True
            self.db.commit()
            return {'acknowledged': True}
        return {'error': 'Alert not found'}
    
    def _update_visibility_record(self, app_id: str, country: str, 
                                   language: str, platform: str):
        """Update visibility record"""
        # Get latest ranking data
        latest = self.db.query(func.max(RankRecord.rank_date)).filter(
            RankRecord.app_id == app_id,
            RankRecord.country == country,
            RankRecord.language == language
        ).scalar()
        
        if not latest:
            return
        
        records = self.db.query(RankRecord).filter(
            RankRecord.app_id == app_id,
            RankRecord.country == country,
            RankRecord.language == language,
            RankRecord.rank_date == latest
        ).all()
        
        if not records:
            return
        
        # Calculate visibility metrics
        tracked = len(records)
        top_3 = len([r for r in records if r.current_position and r.current_position <= 3])
        top_10 = len([r for r in records if r.current_position and r.current_position <= 10])
        top_25 = len([r for r in records if r.current_position and r.current_position <= 25])
        top_50 = len([r for r in records if r.current_position and r.current_position <= 50])
        
        # Calculate visibility score
        visibility_score = self.visibility_scorer.calculate_visibility_score(records)
        
        # Get previous visibility
        prev = self.db.query(VisibilityRecord).filter(
            VisibilityRecord.app_id == app_id,
            VisibilityRecord.country == country,
            VisibilityRecord.language == language
        ).order_by(VisibilityRecord.record_date.desc()).first()
        
        previous_visibility = prev.visibility_score if prev else 0
        visibility_change = visibility_score - previous_visibility if prev else 0
        
        # Create visibility record
        visibility = VisibilityRecord(
            id=uuid.uuid4(),
            app_id=app_id,
            country=country,
            language=language,
            platform=platform,
            visibility_score=visibility_score,
            previous_visibility=previous_visibility,
            visibility_change=visibility_change,
            tracked_keywords=tracked,
            top_3_count=top_3,
            top_10_count=top_10,
            top_25_count=top_25,
            top_50_count=top_50,
            organic_reach_estimate=int(visibility_score * 100),
            record_date=datetime.utcnow()
        )
        
        self.db.add(visibility)
        self.db.commit()
    
    def _rank_record_to_dict(self, record: RankRecord) -> Dict:
        return {
            'id': str(record.id),
            'keyword': record.keyword,
            'country': record.country,
            'language': record.language,
            'current_position': record.current_position,
            'previous_position': record.previous_position,
            'best_position': record.best_position,
            'worst_position': record.worst_position,
            'position_change': record.position_change,
            'visibility_score': record.visibility_score,
            'search_volume': record.search_volume,
            'rank_date': record.rank_date.isoformat(),
            'is_favorite': record.is_favorite
        }
    
    def _alert_to_dict(self, alert: RankAlert) -> Dict:
        return {
            'id': str(alert.id),
            'keyword': alert.keyword,
            'alert_type': alert.alert_type,
            'title': alert.title,
            'description': alert.description,
            'severity': alert.severity,
            'is_read': alert.is_read,
            'alert_date': alert.alert_date.isoformat()
        }
    
    def _get_empty_visibility(self) -> Dict:
        return {
            'visibility_score': 0,
            'previous_visibility': 0,
            'visibility_change': 0,
            'tracked_keywords': 0,
            'top_3_count': 0,
            'top_10_count': 0,
            'top_25_count': 0,
            'top_50_count': 0,
            'organic_reach_estimate': 0,
            'record_date': None
        }
