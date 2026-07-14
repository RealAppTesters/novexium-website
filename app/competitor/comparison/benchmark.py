from typing import Dict, Any, List
from datetime import datetime


class BenchmarkEngine:
    """Compare apps against competitors"""
    
    def compare(self, app_data: Dict, competitor_data: List[Dict]) -> Dict[str, Any]:
        """Compare an app against its competitors"""
        results = {
            'app': {
                'name': app_data.get('name', 'My App'),
                'scores': self._calculate_scores(app_data)
            },
            'competitors': [],
            'benchmarks': {},
            'opportunities': []
        }
        
        for competitor in competitor_data:
            comp_scores = self._calculate_scores(competitor)
            results['competitors'].append({
                'name': competitor.get('name'),
                'scores': comp_scores
            })
            
            # Calculate gaps
            gaps = self._calculate_gaps(app_data, competitor)
            if gaps:
                results['opportunities'].append({
                    'competitor': competitor.get('name'),
                    'gaps': gaps
                })
        
        # Calculate benchmarks
        results['benchmarks'] = self._calculate_benchmarks(competitor_data)
        
        return results
    
    def _calculate_scores(self, data: Dict) -> Dict:
        """Calculate individual scores"""
        return {
            'growth_score': data.get('growth_score', 0),
            'visibility': data.get('visibility_score', 0),
            'rating': data.get('rating', 0),
            'reviews': data.get('review_count', 0),
            'keyword_coverage': data.get('keyword_coverage', 0),
            'creative_score': data.get('creative_score', 0),
            'store_health': data.get('store_health', 0),
            'update_frequency': data.get('update_frequency', 0)
        }
    
    def _calculate_gaps(self, app_data: Dict, competitor: Dict) -> Dict:
        """Calculate gaps between app and competitor"""
        gaps = {}
        
        for key in ['rating', 'visibility_score', 'keyword_coverage', 'creative_score']:
            app_value = app_data.get(key, 0)
            comp_value = competitor.get(key, 0)
            
            if comp_value > app_value:
                gaps[key] = {
                    'gap': comp_value - app_value,
                    'competitor_value': comp_value,
                    'app_value': app_value
                }
        
        return gaps
    
    def _calculate_benchmarks(self, competitor_data: List[Dict]) -> Dict:
        """Calculate benchmarks from competitor data"""
        if not competitor_data:
            return {
                'avg_rating': 0,
                'avg_visibility': 0,
                'avg_keywords': 0,
                'avg_creative': 0,
                'top_competitor': None
            }
        
        avg_rating = sum(c.get('rating', 0) for c in competitor_data) / len(competitor_data)
        avg_visibility = sum(c.get('visibility_score', 0) for c in competitor_data) / len(competitor_data)
        avg_keywords = sum(c.get('keyword_coverage', 0) for c in competitor_data) / len(competitor_data)
        avg_creative = sum(c.get('creative_score', 0) for c in competitor_data) / len(competitor_data)
        
        # Find top competitor (highest growth score)
        top = max(competitor_data, key=lambda x: x.get('growth_score', 0)) if competitor_data else None
        
        return {
            'avg_rating': round(avg_rating, 1),
            'avg_visibility': int(avg_visibility),
            'avg_keywords': int(avg_keywords),
            'avg_creative': int(avg_creative),
            'top_competitor': top.get('name') if top else None
        }
