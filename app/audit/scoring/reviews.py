from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.audit.scoring.base import BaseScorer


class ReviewScorer(BaseScorer):
    """Score reviews and ratings"""
    
    def score(self, data: Dict[str, Any], competitor_data: List[Dict] = None) -> Dict[str, Any]:
        findings = []
        score = 0
        max_score = 0
        
        # 1. Average rating
        average_rating = data.get('average_rating', 0)
        
        if average_rating >= 4.5:
            score += 25
            findings.append({
                'type': 'strength',
                'category': 'reviews',
                'description': f'Excellent rating ({average_rating})',
                'impact': 'high'
            })
        elif average_rating >= 4.0:
            score += 15
            findings.append({
                'type': 'strength',
                'category': 'reviews',
                'description': f'Good rating ({average_rating})',
                'impact': 'medium'
            })
        elif average_rating >= 3.0:
            score += 8
            findings.append({
                'type': 'weakness',
                'category': 'reviews',
                'description': f'Average rating ({average_rating}). Consider addressing user feedback.',
                'impact': 'medium',
                'recommendation': 'Review user feedback and address common issues'
            })
        else:
            score += 2
            findings.append({
                'type': 'weakness',
                'category': 'reviews',
                'description': f'Low rating ({average_rating}). This affects user trust.',
                'impact': 'high',
                'recommendation': 'Prioritize improving user satisfaction'
            })
        max_score += 25
        
        # 2. Review count
        review_count = data.get('review_count', 0)
        
        if review_count >= 100:
            score += 15
            findings.append({
                'type': 'strength',
                'category': 'reviews',
                'description': f'Strong review volume ({review_count} reviews)',
                'impact': 'low'
            })
        elif review_count >= 50:
            score += 10
            findings.append({
                'type': 'strength',
                'category': 'reviews',
                'description': f'Good review volume ({review_count} reviews)',
                'impact': 'low'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'reviews',
                'description': f'Limited reviews ({review_count}). More reviews build trust.',
                'impact': 'medium',
                'recommendation': 'Encourage users to leave reviews'
            })
        max_score += 15
        
        # 3. Review recency
        latest_review_date = data.get('latest_review_date')
        if latest_review_date:
            days_since_latest = (datetime.now() - latest_review_date).days
            if days_since_latest < 7:
                score += 15
                findings.append({
                    'type': 'strength',
                    'category': 'reviews',
                    'description': 'Recent reviews show active engagement',
                    'impact': 'low'
                })
            else:
                score += 5
                findings.append({
                    'type': 'weakness',
                    'category': 'reviews',
                    'description': f'No recent reviews in {days_since_latest} days',
                    'impact': 'medium',
                    'recommendation': 'Encourage users to leave recent reviews'
                })
        max_score += 15
        
        # 4. Sentiment (if available)
        positive_sentiment = data.get('positive_sentiment', 0)
        if positive_sentiment > 0:
            if positive_sentiment >= 0.70:
                score += 20
                findings.append({
                    'type': 'strength',
                    'category': 'reviews',
                    'description': f'Strong positive sentiment ({int(positive_sentiment * 100)}%)',
                    'impact': 'high'
                })
            else:
                score += 10
                findings.append({
                    'type': 'weakness',
                    'category': 'reviews',
                    'description': f'Mixed sentiment ({int(positive_sentiment * 100)}% positive)',
                    'impact': 'medium',
                    'recommendation': 'Address negative feedback to improve sentiment'
                })
        max_score += 20
        
        # 5. Developer response rate
        response_rate = data.get('developer_response_rate', 0)
        if response_rate > 0:
            if response_rate >= 0.60:
                score += 10
                findings.append({
                    'type': 'strength',
                    'category': 'reviews',
                    'description': f'Good developer response rate ({int(response_rate * 100)}%)',
                    'impact': 'low'
                })
            else:
                score += 5
                findings.append({
                    'type': 'weakness',
                    'category': 'reviews',
                    'description': f'Low developer response rate ({int(response_rate * 100)}%)',
                    'impact': 'medium',
                    'recommendation': 'Reply to more user reviews'
                })
        max_score += 10
        
        final_score = self._clamp_score((score / max_score) * 100 if max_score > 0 else 0)
        
        return {
            'score': final_score,
            'findings': findings
        }
