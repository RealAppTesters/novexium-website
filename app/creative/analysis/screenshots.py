from typing import Dict, Any, List
from app.creative.analysis.base import BaseAnalyzer


class ScreenshotAnalyzer(BaseAnalyzer):
    """Analyze screenshots using heuristics"""
    
    def analyze(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        findings = []
        score = 50  # Start at neutral
        max_score = 0
        
        # 1. Check if screenshot exists
        if asset_data.get('url'):
            score += 20
            max_score += 20
            findings.append({
                'type': 'strength',
                'description': 'Screenshot is present',
                'impact': 'low'
            })
        else:
            findings.append({
                'type': 'weakness',
                'description': 'No screenshot found',
                'impact': 'high',
                'recommendation': 'Add screenshots to showcase your app'
            })
            return {'score': 0, 'findings': findings}
        
        # 2. Check dimensions (if available)
        width = asset_data.get('width', 0)
        height = asset_data.get('height', 0)
        
        if width > 0 and height > 0:
            aspect_ratio = width / height
            
            # App Store: 9:16 for phones
            if 0.55 <= aspect_ratio <= 0.58:
                score += 15
                max_score += 15
                findings.append({
                    'type': 'strength',
                    'description': 'Correct aspect ratio for App Store',
                    'impact': 'low'
                })
            else:
                max_score += 15
                findings.append({
                    'type': 'weakness',
                    'description': f'Incorrect aspect ratio ({aspect_ratio:.2f}:1)',
                    'impact': 'medium',
                    'recommendation': 'Use 9:16 aspect ratio for App Store screenshots'
                })
        
        # 3. Check for text content (heuristic)
        if asset_data.get('has_text', False):
            score += 20
            max_score += 20
            findings.append({
                'type': 'strength',
                'description': 'Screenshot includes text content',
                'impact': 'medium'
            })
        else:
            max_score += 20
            findings.append({
                'type': 'weakness',
                'description': 'Screenshot lacks text content',
                'impact': 'medium',
                'recommendation': 'Add text to highlight features'
            })
        
        # 4. Check for visual hierarchy (heuristic)
        if asset_data.get('has_visual_hierarchy', False):
            score += 15
            max_score += 15
            findings.append({
                'type': 'strength',
                'description': 'Good visual hierarchy in screenshot',
                'impact': 'low'
            })
        
        # 5. Color analysis (heuristic)
        if asset_data.get('has_high_contrast', False):
            score += 10
            max_score += 10
            findings.append({
                'type': 'strength',
                'description': 'High contrast colors improve readability',
                'impact': 'low'
            })
        
        final_score = int(round((score / max_score) * 100 if max_score > 0 else 0))
        
        return {
            'score': final_score,
            'findings': findings,
            'metrics': {
                'width': width,
                'height': height,
                'aspect_ratio': width / height if height > 0 else None
            }
        }
