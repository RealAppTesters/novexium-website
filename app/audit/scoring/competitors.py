from typing import Dict, Any, List
from app.audit.scoring.base import BaseScorer


class CompetitorScorer(BaseScorer):
    """Score app against competitors"""
    
    def score(self, data: Dict[str, Any], competitor_data: List[Dict] = None) -> Dict[str, Any]:
        findings = []
        score = 50  # Start at neutral
        
        if not competitor_data:
            return {
                'score': 50,
                'findings': [{
                    'type': 'weakness',
                    'category': 'competitors',
                    'description': 'No competitor data available for comparison',
                    'impact': 'medium',
                    'recommendation': 'Add competitors to track'
                }]
            }
        
        # Compare against competitors
        for competitor in competitor_data:
            # Rating comparison
            app_rating = data.get('average_rating', 0)
            comp_rating = competitor.get('rating', 0)
            
            if app_rating > comp_rating:
                score += 5
            elif app_rating < comp_rating:
                score -= 5
            
            # Review count comparison
            app_reviews = data.get('review_count', 0)
            comp_reviews = competitor.get('review_count', 0)
            
            if app_reviews > comp_reviews:
                score += 2
            elif app_reviews < comp_reviews:
                score -= 2
            
            # Screenshot count comparison
            app_screenshots = data.get('screenshot_count', 0)
            comp_screenshots = competitor.get('screenshot_count', 0)
            
            if app_screenshots > comp_screenshots:
                score += 2
            elif app_screenshots < comp_screenshots:
                score -= 2
        
        # Clamp score
        score = self._clamp_score(score)
        
        if score >= 70:
            findings.append({
                'type': 'strength',
                'category': 'competitors',
                'description': f'Strong performance compared to competitors ({score}%)',
                'impact': 'medium'
            })
        elif score >= 50:
            findings.append({
                'type': 'neutral',
                'category': 'competitors',
                'description': f'Competitive position is average ({score}%)',
                'impact': 'low'
            })
        else:
            findings.append({
                'type': 'weakness',
                'category': 'competitors',
                'description': f'App lags behind competitors ({score}%)',
                'impact': 'high',
                'recommendation': 'Review competitor strategies and identify improvement areas'
            })
        
        return {
            'score': score,
            'findings': findings
        }
