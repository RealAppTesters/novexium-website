from typing import List, Dict, Any
import uuid


class RecommendationGenerator:
    """Generate recommendations from audit findings"""
    
    def generate(self, findings: List[Dict], store_data: Dict, competitor_data: List) -> List[Dict]:
        recommendations = []
        
        for finding in findings:
            if finding.get('type') == 'weakness' and finding.get('recommendation'):
                rec = {
                    'id': str(uuid.uuid4())[:8],
                    'title': finding.get('recommendation'),
                    'description': finding.get('description'),
                    'category': finding.get('category'),
                    'impact': finding.get('impact', 'medium'),
                    'effort': self._estimate_effort(finding),
                    'status': 'pending',
                    'created_at': datetime.now().isoformat()
                }
                recommendations.append(rec)
        
        return recommendations
    
    def _estimate_effort(self, finding: Dict) -> str:
        """Estimate effort based on recommendation type"""
        rec = finding.get('recommendation', '').lower()
        
        if any(word in rec for word in ['title', 'keywords', 'reply', 'respond']):
            return 'low'
        elif any(word in rec for word in ['screenshot', 'icon', 'graphic', 'update', 'description']):
            return 'medium'
        elif any(word in rec for word in ['policy', 'legal', 'compliance', 'localization']):
            return 'high'
        else:
            return 'medium'
