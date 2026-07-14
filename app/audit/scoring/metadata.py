from typing import Dict, Any, List
from app.audit.scoring.base import BaseScorer


class MetadataScorer(BaseScorer):
    """Score app metadata including title, description, release notes"""
    
    def score(self, data: Dict[str, Any], competitor_data: List[Dict] = None) -> Dict[str, Any]:
        findings = []
        score = 0
        max_score = 0
        
        # 1. Title length
        title = data.get('title', '')
        title_length = len(title)
        
        if 20 <= title_length <= 60:
            score += 20
            findings.append({
                'type': 'strength',
                'category': 'metadata',
                'description': f'Title length is optimal ({title_length} characters)',
                'impact': 'medium'
            })
        elif title_length < 20:
            score += 10
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': f'Title is too short ({title_length} characters). Consider adding more keywords.',
                'impact': 'medium',
                'recommendation': 'Expand your title to 20-60 characters'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': f'Title is too long ({title_length} characters). Shorten to improve readability.',
                'impact': 'medium',
                'recommendation': 'Shorten your title to 20-60 characters'
            })
        max_score += 20
        
        # 2. Short description
        has_short_description = data.get('has_short_description', False)
        if has_short_description:
            short_desc = data.get('short_description', '')
            short_desc_len = len(short_desc)
            if 80 <= short_desc_len <= 150:
                score += 15
                findings.append({
                    'type': 'strength',
                    'category': 'metadata',
                    'description': 'Short description is well-optimized',
                    'impact': 'low'
                })
            elif short_desc_len > 0:
                score += 10
                findings.append({
                    'type': 'weakness',
                    'category': 'metadata',
                    'description': f'Short description length ({short_desc_len} characters) could be optimized',
                    'impact': 'low',
                    'recommendation': 'Keep short description between 80-150 characters'
                })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': 'No short description found',
                'impact': 'high',
                'recommendation': 'Add a short description to improve discoverability'
            })
        max_score += 15
        
        # 3. Long description
        has_long_description = data.get('has_long_description', False)
        if has_long_description:
            long_desc = data.get('long_description', '')
            long_desc_len = len(long_desc)
            if long_desc_len > 500:
                score += 15
                findings.append({
                    'type': 'strength',
                    'category': 'metadata',
                    'description': 'Detailed long description with good length',
                    'impact': 'low'
                })
            else:
                score += 8
                findings.append({
                    'type': 'weakness',
                    'category': 'metadata',
                    'description': f'Long description is brief ({long_desc_len} characters)',
                    'impact': 'medium',
                    'recommendation': 'Expand your long description to provide more value'
                })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': 'No long description found',
                'impact': 'high',
                'recommendation': 'Add a detailed description of your app'
            })
        max_score += 15
        
        # 4. Release notes
        has_release_notes = data.get('release_notes') is not None
        if has_release_notes:
            release_notes = data.get('release_notes', '')
            if len(release_notes) > 20:
                score += 10
                findings.append({
                    'type': 'strength',
                    'category': 'metadata',
                    'description': 'Recent release notes are informative',
                    'impact': 'low'
                })
            else:
                score += 5
                findings.append({
                    'type': 'weakness',
                    'category': 'metadata',
                    'description': 'Release notes are brief. Users appreciate detailed updates.',
                    'impact': 'low',
                    'recommendation': 'Add more details to your release notes'
                })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': 'No release notes found for recent updates',
                'impact': 'medium',
                'recommendation': 'Add release notes to inform users about updates'
            })
        max_score += 10
        
        # 5. Privacy policy
        has_privacy_policy = data.get('privacy_policy', False)
        if has_privacy_policy:
            score += 15
            findings.append({
                'type': 'strength',
                'category': 'metadata',
                'description': 'Privacy policy is present',
                'impact': 'low'
            })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': 'No privacy policy found',
                'impact': 'critical',
                'recommendation': 'Add a privacy policy to your app listing'
            })
        max_score += 15
        
        # 6. Call to action in description
        description = data.get('long_description', '') or data.get('short_description', '')
        cta_phrases = ['download', 'try', 'get started', 'join', 'start', 'sign up']
        has_cta = any(phrase in description.lower() for phrase in cta_phrases)
        if has_cta:
            score += 10
            findings.append({
                'type': 'strength',
                'category': 'metadata',
                'description': 'Description includes a call to action',
                'impact': 'low'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'metadata',
                'description': 'Description lacks a clear call to action',
                'impact': 'low',
                'recommendation': 'Add a call to action in your description'
            })
        max_score += 10
        
        final_score = self._clamp_score((score / max_score) * 100)
        
        return {
            'score': final_score,
            'findings': findings
        }
