from typing import Dict, Any, List
from app.audit.scoring.base import BaseScorer


class KeywordScorer(BaseScorer):
    """Score app keywords"""
    
    def score(self, data: Dict[str, Any], competitor_data: List[Dict] = None) -> Dict[str, Any]:
        findings = []
        score = 0
        max_score = 0
        
        # 1. Keyword count
        keywords = data.get('keywords', [])
        keyword_count = len(keywords)
        
        if keyword_count >= 10:
            score += 25
            findings.append({
                'type': 'strength',
                'category': 'keywords',
                'description': f'Good keyword coverage ({keyword_count} keywords)',
                'impact': 'medium'
            })
        elif keyword_count >= 5:
            score += 15
            findings.append({
                'type': 'weakness',
                'category': 'keywords',
                'description': f'Limited keyword coverage ({keyword_count} keywords)',
                'impact': 'medium',
                'recommendation': 'Add more relevant keywords to improve visibility'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'keywords',
                'description': f'Low keyword coverage ({keyword_count} keywords)',
                'impact': 'high',
                'recommendation': 'Research and add more keywords'
            })
        max_score += 25
        
        # 2. Keyword diversity
        unique_keywords = data.get('unique_keywords', keyword_count)
        if unique_keywords == keyword_count and keyword_count > 0:
            score += 20
            findings.append({
                'type': 'strength',
                'category': 'keywords',
                'description': 'Good keyword diversity',
                'impact': 'low'
            })
        elif keyword_count > 0:
            score += 10
            findings.append({
                'type': 'weakness',
                'category': 'keywords',
                'description': 'Some keywords are repetitive',
                'impact': 'low',
                'recommendation': 'Remove duplicate keywords'
            })
        max_score += 20
        
        # 3. Long-tail keywords
        long_tail = data.get('long_tail_keywords', keyword_count)
        if long_tail >= 5:
            score += 15
            findings.append({
                'type': 'strength',
                'category': 'keywords',
                'description': 'Good use of long-tail keywords',
                'impact': 'medium'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'keywords',
                'description': 'Limited long-tail keyword usage',
                'impact': 'medium',
                'recommendation': 'Add more long-tail keywords'
            })
        max_score += 15
        
        # 4. Competitor comparison
        if competitor_data:
            avg_competitor_keywords = sum(c.get('keyword_count', 0) for c in competitor_data) / len(competitor_data) if competitor_data else 0
            
            if keyword_count > avg_competitor_keywords:
                score += 20
                findings.append({
                    'type': 'strength',
                    'category': 'keywords',
                    'description': f'More keywords than competitors ({keyword_count} vs avg {int(avg_competitor_keywords)})',
                    'impact': 'medium'
                })
            else:
                score += 10
                findings.append({
                    'type': 'weakness',
                    'category': 'keywords',
                    'description': f'Fewer keywords than competitors ({keyword_count} vs avg {int(avg_competitor_keywords)})',
                    'impact': 'high',
                    'recommendation': 'Expand your keyword coverage to match competitors'
                })
            max_score += 20
        
        final_score = self._clamp_score((score / max_score) * 100 if max_score > 0 else 0)
        
        return {
            'score': final_score,
            'findings': findings
        }
