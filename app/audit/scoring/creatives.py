from typing import Dict, Any, List
from app.audit.scoring.base import BaseScorer


class CreativeScorer(BaseScorer):
    """Score creative assets including screenshots, icons, and videos"""
    
    def score(self, data: Dict[str, Any], competitor_data: List[Dict] = None) -> Dict[str, Any]:
        findings = []
        score = 0
        max_score = 0
        
        # 1. Icon presence
        has_icon = data.get('icon_url') is not None
        if has_icon:
            score += 20
            findings.append({
                'type': 'strength',
                'category': 'creatives',
                'description': 'App icon is present',
                'impact': 'low'
            })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'creatives',
                'description': 'No app icon found',
                'impact': 'critical',
                'recommendation': 'Upload a professional app icon'
            })
        max_score += 20
        
        # 2. Screenshot count
        screenshot_count = data.get('screenshot_count', 0)
        
        if screenshot_count >= 5:
            score += 25
            findings.append({
                'type': 'strength',
                'category': 'creatives',
                'description': f'Good screenshot coverage ({screenshot_count} screenshots)',
                'impact': 'medium'
            })
        elif screenshot_count >= 3:
            score += 15
            findings.append({
                'type': 'weakness',
                'category': 'creatives',
                'description': f'Limited screenshots ({screenshot_count}). More screenshots help with conversion.',
                'impact': 'medium',
                'recommendation': 'Add more screenshots to showcase your app'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'creatives',
                'description': f'Very few screenshots ({screenshot_count}). This may hurt conversion.',
                'impact': 'high',
                'recommendation': 'Add at least 3-5 screenshots'
            })
        max_score += 25
        
        # 3. Screenshot order
        screenshot_order = data.get('screenshot_order', '')
        if screenshot_order == 'good':
            score += 15
            findings.append({
                'type': 'strength',
                'category': 'creatives',
                'description': 'Screenshots are well-ordered',
                'impact': 'low'
            })
        else:
            score += 5
            findings.append({
                'type': 'weakness',
                'category': 'creatives',
                'description': 'Screenshot order could be improved',
                'impact': 'low',
                'recommendation': 'Re-order screenshots to highlight key features first'
            })
        max_score += 15
        
        # 4. Feature graphic (Google Play)
        has_feature_graphic = data.get('has_feature_graphic', False)
        if has_feature_graphic:
            score += 10
            findings.append({
                'type': 'strength',
                'category': 'creatives',
                'description': 'Feature graphic is present',
                'impact': 'low'
            })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'creatives',
                'description': 'No feature graphic found. This can hurt visibility.',
                'impact': 'medium',
                'recommendation': 'Add a feature graphic'
            })
        max_score += 10
        
        # 5. Preview video
        has_preview_video = data.get('has_preview_video', False)
        if has_preview_video:
            score += 10
            findings.append({
                'type': 'strength',
                'category': 'creatives',
                'description': 'Preview video is present',
                'impact': 'low'
            })
        else:
            score += 0
            findings.append({
                'type': 'weakness',
                'category': 'creatives',
                'description': 'No preview video found',
                'impact': 'medium',
                'recommendation': 'Add a preview video to improve conversion'
            })
        max_score += 10
        
        # 6. Competitor comparison
        if competitor_data:
            avg_competitor_screenshots = sum(c.get('screenshot_count', 0) for c in competitor_data) / len(competitor_data) if competitor_data else 0
            
            if screenshot_count >= avg_competitor_screenshots:
                score += 10
                findings.append({
                    'type': 'strength',
                    'category': 'creatives',
                    'description': f'Screenshot count matches or exceeds competitors ({screenshot_count} vs avg {int(avg_competitor_screenshots)})',
                    'impact': 'low'
                })
            else:
                score += 5
                findings.append({
                    'type': 'weakness',
                    'category': 'creatives',
                    'description': f'Fewer screenshots than competitors ({screenshot_count} vs avg {int(avg_competitor_screenshots)})',
                    'impact': 'medium',
                    'recommendation': 'Add more screenshots to stay competitive'
                })
            max_score += 10
        
        final_score = self._clamp_score((score / max_score) * 100 if max_score > 0 else 0)
        
        return {
            'score': final_score,
            'findings': findings
        }
