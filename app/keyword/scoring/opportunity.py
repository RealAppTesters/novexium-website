from typing import Dict, Any


class OpportunityScorer:
    """Calculate keyword opportunity scores"""
    
    def score(self, keyword: Dict[str, Any]) -> int:
        """
        Calculate opportunity score from 0-100
        
        Factors:
        - Search volume (higher is better, but diminishing returns)
        - Competition (lower is better)
        - Difficulty (lower is better)
        - Trend (trending up is better)
        - Relevance to app (if available)
        """
        score = 0
        weights = {
            'volume': 30,
            'competition': 25,
            'difficulty': 25,
            'trend': 20
        }
        
        # Search volume (diminishing returns)
        volume = keyword.get('search_volume', 0)
        if volume > 10000:
            volume_score = 30
        elif volume > 5000:
            volume_score = 25
        elif volume > 1000:
            volume_score = 18
        elif volume > 500:
            volume_score = 12
        elif volume > 100:
            volume_score = 6
        else:
            volume_score = 2
        score += (volume_score / 30) * weights['volume']
        
        # Competition (lower is better)
        competition = keyword.get('competition', 'medium')
        comp_scores = {
            'low': 25,
            'medium': 15,
            'high': 5
        }
        score += (comp_scores.get(competition, 15) / 25) * weights['competition']
        
        # Difficulty (lower is better)
        difficulty = keyword.get('difficulty', 50)
        difficulty_score = max(0, 100 - difficulty) / 100 * 25
        score += (difficulty_score / 25) * weights['difficulty']
        
        # Trend (trending up is better)
        trend = keyword.get('trend_direction', 'stable')
        trend_scores = {
            'up': 20,
            'stable': 10,
            'down': 0
        }
        score += (trend_scores.get(trend, 10) / 20) * weights['trend']
        
        return int(round(score))
