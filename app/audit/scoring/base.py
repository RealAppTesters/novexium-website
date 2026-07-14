from typing import Dict, Any, List, Tuple
from abc import ABC, abstractmethod


class BaseScorer(ABC):
    """Base class for all scoring modules"""
    
    @abstractmethod
    def score(self, data: Dict[str, Any], competitor_data: List[Dict] = None) -> Dict[str, Any]:
        """
        Score the given data and return score and findings
        
        Returns:
            {
                'score': int (0-100),
                'findings': [
                    {
                        'type': 'strength' | 'weakness',
                        'category': str,
                        'description': str,
                        'impact': 'critical' | 'high' | 'medium' | 'low',
                        'recommendation': str (optional)
                    }
                ]
            }
        """
        pass
    
    def _clamp_score(self, value: float, min_val: int = 0, max_val: int = 100) -> int:
        """Clamp a score between min and max values"""
        return int(round(max(min_val, min(max_val, value))))
