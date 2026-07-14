from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
import uuid

from app.models.keyword import Keyword
from app.models.app_keyword import AppKeyword
from app.models.keyword_ranking import KeywordRanking
from app.models.keyword_group import KeywordGroup
from app.keyword.scoring.opportunity import OpportunityScorer
from app.keyword.scoring.difficulty import DifficultyScorer
from app.keyword.scoring.trend import TrendAnalyzer


class KeywordService:
    def __init__(self, db: Session):
        self.db = db
        self.opportunity_scorer = OpportunityScorer()
        self.difficulty_scorer = DifficultyScorer()
        self.trend_analyzer = TrendAnalyzer()
    
    def get_keyword_dashboard(self, app_id: str) -> Dict[str, Any]:
        """Get keyword dashboard data for an app"""
        app_keywords = self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id,
            AppKeyword.is_tracked == True
        ).all()
        
        tracked_count = len(app_keywords)
        
        if tracked_count == 0:
            return {
                'tracked_count': 0,
                'avg_ranking': None,
                'ranking_change': None,
                'opportunities': [],
                'quick_wins': [],
                'recent_changes': []
            }
        
        # Calculate average ranking
        rankings = [ak.current_ranking for ak in app_keywords if ak.current_ranking]
        avg_ranking = sum(rankings) / len(rankings) if rankings else None
        
        # Calculate ranking change
        changes = [ak.ranking_change for ak in app_keywords if ak.ranking_change]
        avg_change = sum(changes) / len(changes) if changes else None
        
        # Find opportunities (keywords with high opportunity score)
        opportunities = self.db.query(Keyword).filter(
            Keyword.opportunity_score >= 70
        ).limit(5).all()
        
        # Find quick wins (keywords with low difficulty and good potential)
        quick_wins = self.db.query(Keyword).filter(
            Keyword.difficulty <= 30,
            Keyword.opportunity_score >= 50
        ).limit(3).all()
        
        # Recent changes
        recent_changes = self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id,
            AppKeyword.ranking_date >= datetime.now() - timedelta(days=7)
        ).order_by(AppKeyword.ranking_date.desc()).limit(5).all()
        
        return {
            'tracked_count': tracked_count,
            'avg_ranking': int(avg_ranking) if avg_ranking else None,
            'ranking_change': int(avg_change) if avg_change else None,
            'opportunities': [self._keyword_to_dict(k) for k in opportunities],
            'quick_wins': [self._keyword_to_dict(k) for k in quick_wins],
            'recent_changes': [self._app_keyword_to_dict(ak) for ak in recent_changes]
        }
    
    def search_keywords(self, query: str, app_id: str = None, 
                        filters: Dict = None, sort_by: str = 'opportunity',
                        limit: int = 50) -> List[Dict]:
        """Search for keywords with filters"""
        search_query = self.db.query(Keyword)
        
        if query:
            search_query = search_query.filter(Keyword.keyword.ilike(f'%{query}%'))
        
        if filters:
            if filters.get('country'):
                search_query = search_query.filter(Keyword.country == filters['country'])
            if filters.get('language'):
                search_query = search_query.filter(Keyword.language == filters['language'])
            if filters.get('min_volume'):
                search_query = search_query.filter(Keyword.search_volume >= filters['min_volume'])
            if filters.get('max_difficulty'):
                search_query = search_query.filter(Keyword.difficulty <= filters['max_difficulty'])
        
        # Sorting
        sort_mapping = {
            'opportunity': Keyword.opportunity_score.desc(),
            'volume': Keyword.search_volume.desc(),
            'difficulty': Keyword.difficulty.asc(),
            'traffic': Keyword.estimated_traffic.desc(),
            'alphabetical': Keyword.keyword.asc()
        }
        search_query = search_query.order_by(sort_mapping.get(sort_by, Keyword.opportunity_score.desc()))
        
        keywords = search_query.limit(limit).all()
        
        # If app_id provided, get rankings
        if app_id:
            app_keywords = {ak.keyword_id: ak for ak in self.db.query(AppKeyword).filter(
                AppKeyword.app_id == app_id
            ).all()}
            
            for k in keywords:
                if k.id in app_keywords:
                    ak = app_keywords[k.id]
                    k.current_ranking = ak.current_ranking
                    k.previous_ranking = ak.previous_ranking
                    k.ranking_change = ak.ranking_change
                else:
                    k.current_ranking = None
                    k.previous_ranking = None
                    k.ranking_change = None
        
        return [self._keyword_to_dict(k) for k in keywords]
    
    def get_opportunities(self, app_id: str) -> List[Dict]:
        """Get keyword opportunities for an app"""
        # Find keywords with high opportunity that the app doesn't track
        tracked_keyword_ids = [ak.keyword_id for ak in self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id
        ).all()]
        
        opportunities = self.db.query(Keyword).filter(
            Keyword.opportunity_score >= 60,
            ~Keyword.id.in_(tracked_keyword_ids)
        ).order_by(Keyword.opportunity_score.desc()).limit(20).all()
        
        return [self._keyword_to_dict(k) for k in opportunities]
    
    def get_competitor_keywords(self, app_id: str, competitor_app_id: str) -> Dict:
        """Get competitor keywords comparison"""
        # Get user's tracked keywords
        user_keywords = {ak.keyword_id for ak in self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id
        ).all()}
        
        # Get competitor's tracked keywords
        competitor_keywords = {ak.keyword_id for ak in self.db.query(AppKeyword).filter(
            AppKeyword.app_id == competitor_app_id
        ).all()}
        
        # Find shared keywords
        shared = user_keywords & competitor_keywords
        
        # Find unique to competitor
        competitor_unique = competitor_keywords - user_keywords
        
        # Find unique to user
        user_unique = user_keywords - competitor_keywords
        
        return {
            'shared_count': len(shared),
            'competitor_unique_count': len(competitor_unique),
            'user_unique_count': len(user_unique),
            'shared_keywords': [self._get_keyword_details(k_id) for k_id in list(shared)[:10]],
            'competitor_unique_keywords': [self._get_keyword_details(k_id) for k_id in list(competitor_unique)[:10]],
            'potential_opportunities': [self._get_keyword_details(k_id) for k_id in list(competitor_unique)[:5] 
                                       if self._check_keyword_opportunity(k_id)]
        }
    
    def track_keyword(self, app_id: str, keyword_id: str) -> Dict:
        """Start tracking a keyword for an app"""
        # Check if already tracking
        existing = self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id,
            AppKeyword.keyword_id == keyword_id
        ).first()
        
        if existing:
            existing.is_tracked = True
            self.db.commit()
            return {'status': 'already_tracking'}
        
        # Get current ranking (mock)
        current_ranking = self._get_mock_ranking(keyword_id)
        
        app_keyword = AppKeyword(
            id=uuid.uuid4(),
            app_id=app_id,
            keyword_id=keyword_id,
            current_ranking=current_ranking,
            previous_ranking=current_ranking,
            best_ranking=current_ranking,
            worst_ranking=current_ranking,
            ranking_change=0,
            ranking_date=datetime.now(),
            is_tracked=True
        )
        
        self.db.add(app_keyword)
        self.db.commit()
        
        return {'status': 'tracking_started', 'keyword_id': keyword_id}
    
    def untrack_keyword(self, app_id: str, keyword_id: str) -> Dict:
        """Stop tracking a keyword"""
        app_keyword = self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id,
            AppKeyword.keyword_id == keyword_id
        ).first()
        
        if app_keyword:
            app_keyword.is_tracked = False
            self.db.commit()
            return {'status': 'untracked'}
        
        return {'status': 'not_found'}
    
    def get_keyword_history(self, app_id: str, keyword_id: str, 
                            days: int = 30) -> List[Dict]:
        """Get ranking history for a keyword"""
        app_keyword = self.db.query(AppKeyword).filter(
            AppKeyword.app_id == app_id,
            AppKeyword.keyword_id == keyword_id
        ).first()
        
        if not app_keyword:
            return []
        
        cutoff = datetime.now() - timedelta(days=days)
        rankings = self.db.query(KeywordRanking).filter(
            KeywordRanking.app_keyword_id == app_keyword.id,
            KeywordRanking.ranking_date >= cutoff
        ).order_by(KeywordRanking.ranking_date.asc()).all()
        
        return [{
            'ranking': r.ranking,
            'date': r.ranking_date.isoformat()
        } for r in rankings]
    
    def _keyword_to_dict(self, keyword: Keyword) -> Dict:
        """Convert keyword to dict"""
        return {
            'id': str(keyword.id),
            'keyword': keyword.keyword,
            'search_volume': keyword.search_volume,
            'difficulty': keyword.difficulty,
            'opportunity_score': keyword.opportunity_score,
            'estimated_traffic': keyword.estimated_traffic,
            'competition': keyword.competition,
            'country': keyword.country,
            'language': keyword.language,
            'is_trending': keyword.is_trending,
            'trend_direction': keyword.trend_direction,
            'last_updated': keyword.last_updated.isoformat() if keyword.last_updated else None
        }
    
    def _app_keyword_to_dict(self, app_keyword: AppKeyword) -> Dict:
        """Convert app_keyword to dict"""
        return {
            'keyword': app_keyword.keyword.keyword,
            'current_ranking': app_keyword.current_ranking,
            'previous_ranking': app_keyword.previous_ranking,
            'ranking_change': app_keyword.ranking_change,
            'date': app_keyword.ranking_date.isoformat()
        }
    
    def _get_keyword_details(self, keyword_id: str) -> Dict:
        """Get keyword details by ID"""
        keyword = self.db.query(Keyword).filter(Keyword.id == keyword_id).first()
        return self._keyword_to_dict(keyword) if keyword else {}
    
    def _check_keyword_opportunity(self, keyword_id: str) -> bool:
        """Check if a keyword is a good opportunity"""
        keyword = self.db.query(Keyword).filter(Keyword.id == keyword_id).first()
        return keyword and keyword.opportunity_score >= 50
    
    def _get_mock_ranking(self, keyword_id: str) -> int:
        """Get mock ranking for a keyword"""
        import random
        return random.randint(1, 100)
