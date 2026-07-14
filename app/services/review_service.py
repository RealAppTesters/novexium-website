from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
import uuid

from app.models.review import Review
from app.models.review_theme import ReviewTheme
from app.models.review_insight import ReviewInsight
from app.review.retrieval.app_store import AppStoreReviewRetriever
from app.review.retrieval.google_play import GooglePlayReviewRetriever
from app.review.classification.sentiment import SentimentAnalyzer
from app.review.classification.themes import ThemeClassifier
from app.review.analysis.trends import TrendAnalyzer
from app.review.analysis.insights import InsightGenerator
from app.review.response.drafts import ResponseDraftGenerator


class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.retrievers = {
            'app_store': AppStoreReviewRetriever(),
            'google_play': GooglePlayReviewRetriever()
        }
        self.sentiment_analyzer = SentimentAnalyzer()
        self.theme_classifier = ThemeClassifier()
        self.trend_analyzer = TrendAnalyzer()
        self.insight_generator = InsightGenerator()
        self.response_generator = ResponseDraftGenerator()
    
    def retrieve_reviews(self, app_id: str, platform: str, limit: int = 100) -> Dict[str, Any]:
        """Retrieve reviews from the store"""
        retriever = self.retrievers.get(platform)
        if not retriever:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Fetch reviews
        reviews_data = retriever.retrieve_reviews(app_id, limit)
        
        saved = []
        for review_data in reviews_data:
            # Check if review already exists
            existing = self.db.query(Review).filter(
                Review.review_id == review_data['review_id']
            ).first()
            
            if existing:
                # Update if changed
                if existing.content != review_data.get('content'):
                    existing.content = review_data.get('content')
                    existing.rating = review_data.get('rating')
                    existing.review_date = review_data.get('review_date')
                    existing.is_processed = False
                    self.db.commit()
                saved.append(existing)
                continue
            
            # Analyze sentiment
            sentiment = self.sentiment_analyzer.analyze(
                review_data.get('content', ''),
                review_data.get('rating', 0)
            )
            
            # Classify themes
            themes = self.theme_classifier.classify(review_data.get('content', ''))
            
            # Create review
            review = Review(
                id=uuid.uuid4(),
                app_id=app_id,
                review_id=review_data['review_id'],
                reviewer=review_data.get('reviewer'),
                rating=review_data.get('rating'),
                title=review_data.get('title'),
                content=review_data.get('content'),
                sentiment=sentiment['label'],
                sentiment_score=sentiment['score'],
                theme=themes['primary'] if themes else None,
                categories=themes['all'] if themes else [],
                language=review_data.get('language'),
                country=review_data.get('country'),
                version=review_data.get('version'),
                review_date=review_data.get('review_date'),
                is_responded=review_data.get('is_responded', False),
                response=review_data.get('response'),
                response_date=review_data.get('response_date'),
                is_processed=True
            )
            
            self.db.add(review)
            saved.append(review)
            
            # Update theme counts
            self._update_theme_counts(app_id, themes, sentiment['label'])
        
        self.db.commit()
        
        return {
            'total': len(saved),
            'new': len([r for r in saved if not hasattr(r, '_existing')]),
            'updated': len([r for r in saved if hasattr(r, '_existing')])
        }
    
    def get_reviews(self, app_id: str, filters: Dict = None, 
                    sort_by: str = 'date', limit: int = 50) -> List[Dict]:
        """Get reviews with filters"""
        query = self.db.query(Review).filter(Review.app_id == app_id)
        
        if filters:
            if filters.get('rating'):
                query = query.filter(Review.rating.in_(filters['rating']))
            if filters.get('sentiment'):
                query = query.filter(Review.sentiment.in_(filters['sentiment']))
            if filters.get('theme'):
                query = query.filter(Review.theme.in_(filters['theme']))
            if filters.get('language'):
                query = query.filter(Review.language == filters['language'])
            if filters.get('country'):
                query = query.filter(Review.country == filters['country'])
            if filters.get('version'):
                query = query.filter(Review.version == filters['version'])
            if filters.get('bookmarked'):
                query = query.filter(Review.is_bookmarked == True)
            if filters.get('unresponded'):
                query = query.filter(Review.is_responded == False)
        
        # Sorting
        sort_mapping = {
            'date': Review.review_date.desc(),
            'oldest': Review.review_date.asc(),
            'rating': Review.rating.desc(),
            'rating_low': Review.rating.asc(),
            'sentiment': Review.sentiment_score.desc()
        }
        query = query.order_by(sort_mapping.get(sort_by, Review.review_date.desc()))
        
        reviews = query.limit(limit).all()
        return [self._review_to_dict(r) for r in reviews]
    
    def get_dashboard(self, app_id: str) -> Dict[str, Any]:
        """Get review dashboard data"""
        reviews = self.db.query(Review).filter(Review.app_id == app_id).all()
        
        if not reviews:
            return {
                'total_reviews': 0,
                'average_rating': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'unresponded_count': 0,
                'recent_activity': [],
                'themes': []
            }
        
        total = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / total
        
        positive = len([r for r in reviews if r.sentiment == 'positive'])
        negative = len([r for r in reviews if r.sentiment == 'negative'])
        neutral = len([r for r in reviews if r.sentiment == 'neutral'])
        unresponded = len([r for r in reviews if not r.is_responded])
        
        # Recent activity
        recent = sorted(reviews, key=lambda x: x.review_date, reverse=True)[:10]
        
        # Theme distribution
        themes = self.db.query(ReviewTheme).filter(
            ReviewTheme.app_id == app_id
        ).order_by(ReviewTheme.review_count.desc()).limit(10).all()
        
        return {
            'total_reviews': total,
            'average_rating': round(avg_rating, 1),
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'unresponded_count': unresponded,
            'recent_activity': [self._review_to_dict(r) for r in recent],
            'themes': [self._theme_to_dict(t) for t in themes]
        }
    
    def generate_insights(self, app_id: str) -> List[Dict]:
        """Generate insights from reviews"""
        reviews = self.db.query(Review).filter(
            Review.app_id == app_id,
            Review.is_processed == True
        ).all()
        
        if not reviews:
            return []
        
        # Get existing insights
        existing = self.db.query(ReviewInsight).filter(
            ReviewInsight.app_id == app_id
        ).all()
        
        # Generate new insights
        insights = self.insight_generator.generate(reviews, existing)
        
        # Save new insights
        saved = []
        for insight_data in insights:
            insight = ReviewInsight(
                id=uuid.uuid4(),
                app_id=app_id,
                insight_type=insight_data['type'],
                title=insight_data['title'],
                description=insight_data.get('description'),
                impact=insight_data.get('impact'),
                supporting_reviews=insight_data.get('supporting_reviews', []),
                supporting_count=len(insight_data.get('supporting_reviews', [])),
                sentiment=insight_data.get('sentiment'),
                recommendation=insight_data.get('recommendation'),
                detected_date=datetime.utcnow()
            )
            self.db.add(insight)
            saved.append(insight)
        
        self.db.commit()
        
        return [self._insight_to_dict(i) for i in saved]
    
    def generate_response_draft(self, review_id: str) -> Dict[str, Any]:
        """Generate a response draft for a review"""
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return None
        
        draft = self.response_generator.generate(review)
        
        return {
            'review_id': str(review.id),
            'draft': draft,
            'rating': review.rating,
            'sentiment': review.sentiment
        }
    
    def bookmark_review(self, review_id: str) -> Dict:
        """Bookmark a review"""
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if review:
            review.is_bookmarked = not review.is_bookmarked
            self.db.commit()
            return {'bookmarked': review.is_bookmarked}
        return {'error': 'Review not found'}
    
    def _review_to_dict(self, review: Review) -> Dict:
        return {
            'id': str(review.id),
            'reviewer': review.reviewer,
            'rating': review.rating,
            'title': review.title,
            'content': review.content,
            'sentiment': review.sentiment,
            'sentiment_score': review.sentiment_score,
            'theme': review.theme,
            'categories': review.categories,
            'language': review.language,
            'country': review.country,
            'version': review.version,
            'review_date': review.review_date.isoformat(),
            'is_responded': review.is_responded,
            'response': review.response,
            'response_date': review.response_date.isoformat() if review.response_date else None,
            'is_bookmarked': review.is_bookmarked
        }
    
    def _theme_to_dict(self, theme: ReviewTheme) -> Dict:
        return {
            'id': str(theme.id),
            'theme': theme.theme,
            'review_count': theme.review_count,
            'positive_count': theme.positive_count,
            'negative_count': theme.negative_count,
            'neutral_count': theme.neutral_count,
            'average_rating': theme.average_rating,
            'trend': theme.trend
        }
    
    def _insight_to_dict(self, insight: ReviewInsight) -> Dict:
        return {
            'id': str(insight.id),
            'type': insight.insight_type,
            'title': insight.title,
            'description': insight.description,
            'impact': insight.impact,
            'supporting_count': insight.supporting_count,
            'recommendation': insight.recommendation,
            'detected_date': insight.detected_date.isoformat()
        }
    
    def _update_theme_counts(self, app_id: str, themes: Dict, sentiment: str):
        """Update theme counts"""
        if not themes:
            return
        
        primary = themes.get('primary')
        if primary:
            theme = self.db.query(ReviewTheme).filter(
                ReviewTheme.app_id == app_id,
                ReviewTheme.theme == primary
            ).first()
            
            if not theme:
                theme = ReviewTheme(
                    id=uuid.uuid4(),
                    app_id=app_id,
                    theme=primary,
                    review_count=0,
                    positive_count=0,
                    negative_count=0,
                    neutral_count=0,
                    last_detected=datetime.utcnow()
                )
                self.db.add(theme)
            
            theme.review_count += 1
            if sentiment == 'positive':
                theme.positive_count += 1
            elif sentiment == 'negative':
                theme.negative_count += 1
            else:
                theme.neutral_count += 1
            
            # Recalculate average rating
            reviews = self.db.query(Review).filter(
                Review.app_id == app_id,
                Review.theme == primary
            ).all()
            if reviews:
                theme.average_rating = sum(r.rating for r in reviews) / len(reviews)
            
            theme.last_detected = datetime.utcnow()
