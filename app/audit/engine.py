from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.audit.scoring.metadata import MetadataScorer
from app.audit.scoring.keywords import KeywordScorer
from app.audit.scoring.creatives import CreativeScorer
from app.audit.scoring.reviews import ReviewScorer
from app.audit.scoring.competitors import CompetitorScorer
from app.audit.scoring.store_health import StoreHealthScorer
from app.audit.rules.metadata_rules import MetadataRules
from app.audit.rules.keyword_rules import KeywordRules
from app.audit.rules.creative_rules import CreativeRules
from app.audit.rules.review_rules import ReviewRules
from app.audit.rules.store_rules import StoreRules
from app.audit.recommendations.generator import RecommendationGenerator
from app.audit.recommendations.prioritizer import Prioritizer
from app.models.audit import Audit
from app.models.app import App


class AuditEngine:
    """Main audit orchestrator"""
    
    def __init__(self, db: Session):
        self.db = db
        self.scorers = {
            'metadata': MetadataScorer(),
            'keywords': KeywordScorer(),
            'creatives': CreativeScorer(),
            'reviews': ReviewScorer(),
            'competitors': CompetitorScorer(),
            'store_health': StoreHealthScorer()
        }
        self.rules = {
            'metadata': MetadataRules(),
            'keywords': KeywordRules(),
            'creatives': CreativeRules(),
            'reviews': ReviewRules(),
            'store_health': StoreRules()
        }
        self.recommendation_generator = RecommendationGenerator()
        self.prioritizer = Prioritizer()
    
    def run_audit(self, app_id: str, user_id: str) -> Dict[str, Any]:
        """Run a complete audit for an app"""
        
        # Get app data
        app = self.db.query(App).filter(App.id == app_id).first()
        if not app:
            raise ValueError(f"App {app_id} not found")
        
        # Fetch store data (mock for now)
        store_data = self._fetch_store_data(app)
        
        # Fetch competitor data (mock for now)
        competitor_data = self._fetch_competitor_data(app)
        
        # Run scorers
        scores = {}
        findings = {}
        
        for category, scorer in self.scorers.items():
            category_data = store_data.get(category, {})
            category_scores = scorer.score(category_data, competitor_data)
            scores[category] = category_scores['score']
            findings[category] = category_scores['findings']
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(scores)
        
        # Generate rules-based findings
        rule_findings = self._apply_rules(store_data, competitor_data)
        
        # Combine all findings
        all_findings = self._merge_findings(findings, rule_findings)
        
        # Generate recommendations
        recommendations = self.recommendation_generator.generate(
            all_findings,
            store_data,
            competitor_data
        )
        
        # Prioritize recommendations
        prioritized = self.prioritizer.prioritize(recommendations)
        
        # Determine next win
        next_win = prioritized[0] if prioritized else None
        
        # Determine quick wins
        quick_wins = [r for r in prioritized if r.get('effort') == 'low'][:3]
        
        # Create audit record
        audit = Audit(
            id=uuid.uuid4(),
            app_id=app_id,
            user_id=user_id,
            overall_score=overall_score,
            metadata_score=scores.get('metadata', 0),
            keyword_score=scores.get('keywords', 0),
            creative_score=scores.get('creatives', 0),
            review_score=scores.get('reviews', 0),
            competitor_score=scores.get('competitors', 0),
            store_health_score=scores.get('store_health', 0),
            findings=all_findings,
            recommendations=prioritized,
            next_win=next_win,
            quick_wins=quick_wins,
            audit_date=datetime.utcnow()
        )
        
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)
        
        return {
            'audit_id': str(audit.id),
            'overall_score': overall_score,
            'scores': scores,
            'findings': all_findings,
            'recommendations': prioritized,
            'next_win': next_win,
            'quick_wins': quick_wins,
            'audit_date': audit.audit_date.isoformat()
        }
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> int:
        """Calculate weighted overall score"""
        weights = {
            'metadata': 0.20,
            'keywords': 0.20,
            'creatives': 0.15,
            'reviews': 0.15,
            'competitors': 0.15,
            'store_health': 0.15
        }
        
        total = sum(scores.get(cat, 0) * weight for cat, weight in weights.items())
        return int(round(total))
    
    def _fetch_store_data(self, app: App) -> Dict[str, Any]:
        """Fetch app store data (mock implementation)"""
        # In production, this would call the App Store/Google Play APIs
        return {
            'metadata': {
                'title': app.app_name,
                'title_length': len(app.app_name),
                'short_description': "Track your fitness journey with our intuitive app",
                'long_description': "This is a powerful fitness tracking app that helps users achieve their health goals with intuitive features and real-time insights.",
                'release_notes': "Bug fixes and performance improvements",
                'privacy_policy': True,
                'has_short_description': True,
                'has_long_description': True
            },
            'keywords': {
                'keywords': ['fitness', 'tracker', 'health', 'workout', 'exercise'],
                'keyword_count': 5,
                'unique_keywords': 5
            },
            'creatives': {
                'icon_url': None,
                'screenshot_count': 5,
                'screenshot_order': 'good',
                'has_feature_graphic': True,
                'has_preview_video': False
            },
            'reviews': {
                'average_rating': 4.8,
                'review_count': 247,
                'latest_review_date': datetime.now() - timedelta(days=1),
                'positive_sentiment': 0.85,
                'negative_sentiment': 0.05,
                'developer_response_rate': 0.70
            },
            'store_health': {
                'last_updated': datetime.now() - timedelta(days=30),
                'has_privacy_policy': True,
                'has_terms': True,
                'localization_count': 3,
                'update_frequency': 'monthly'
            }
        }
    
    def _fetch_competitor_data(self, app: App) -> List[Dict[str, Any]]:
        """Fetch competitor data (mock implementation)"""
        return [
            {
                'name': 'FitApp Pro',
                'rating': 4.7,
                'review_count': 189,
                'keyword_count': 8,
                'screenshot_count': 6,
                'update_frequency': 'weekly'
            },
            {
                'name': 'HealthTracker',
                'rating': 4.5,
                'review_count': 312,
                'keyword_count': 6,
                'screenshot_count': 4,
                'update_frequency': 'monthly'
            }
        ]
    
    def _apply_rules(self, store_data: Dict, competitor_data: List) -> List[Dict]:
        """Apply all rules to generate findings"""
        all_findings = []
        
        for category, rules in self.rules.items():
            category_data = store_data.get(category, {})
            findings = rules.apply(category_data, competitor_data)
            all_findings.extend(findings)
        
        return all_findings
    
    def _merge_findings(self, scorer_findings: Dict, rule_findings: List) -> List[Dict]:
        """Merge findings from scorers and rules"""
        merged = []
        
        # Add scorer findings
        for category, findings in scorer_findings.items():
            for finding in findings:
                finding['category'] = category
                merged.append(finding)
        
        # Add rule findings
        for finding in rule_findings:
            merged.append(finding)
        
        return merged
