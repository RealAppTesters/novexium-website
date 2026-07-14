from typing import Dict, Any


class TitleScorer:
    """Score app titles"""
    
    def score(self, title: str, platform: str = 'app_store') -> int:
        score = 0
        max_score = 0
        
        # 1. Length check
        length = len(title)
        if platform == 'app_store':
            optimal_min, optimal_max = 20, 30
            max_allowed = 30
        else:  # google_play
            optimal_min, optimal_max = 25, 50
            max_allowed = 50
        
        if optimal_min <= length <= optimal_max:
            score += 40
            max_score += 40
        elif length <= max_allowed:
            score += 25
            max_score += 40
        else:
            score += 10
            max_score += 40
        
        # 2. Keyword presence
        keyword_count = self._count_keywords(title)
        if keyword_count >= 2:
            score += 30
        elif keyword_count >= 1:
            score += 15
        max_score += 30
        
        # 3. Readability
        if self._is_readable(title):
            score += 20
        else:
            score += 5
        max_score += 20
        
        # 4. Capitalization
        if self._has_proper_capitalization(title):
            score += 10
        max_score += 10
        
        return int(round((score / max_score) * 100 if max_score > 0 else 0))
    
    def _count_keywords(self, text: str) -> int:
        """Count potential keywords in title"""
        # Simple word count - in production, use actual keyword detection
        words = text.split()
        return len([w for w in words if len(w) > 3])
    
    def _is_readable(self, text: str) -> bool:
        """Check if title is readable"""
        words = text.split()
        return len(words) <= 8
    
    def _has_proper_capitalization(self, text: str) -> bool:
        """Check if title has proper capitalization"""
        # App Store: proper case, Google Play: sentence case or proper case
        return text[0].isupper()
