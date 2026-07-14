from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.creative_asset import CreativeAsset
from app.models.creative_analysis import CreativeAnalysis
from app.models.creative_history import CreativeHistory
from app.creative.retrieval.app_store import AppStoreRetriever
from app.creative.retrieval.google_play import GooglePlayRetriever
from app.creative.analysis.screenshots import ScreenshotAnalyzer
from app.creative.analysis.icon import IconAnalyzer
from app.creative.analysis.feature_graphic import FeatureGraphicAnalyzer
from app.creative.scoring.creative_scorer import CreativeScorer


class CreativeService:
    def __init__(self, db: Session):
        self.db = db
        self.retrievers = {
            'app_store': AppStoreRetriever(),
            'google_play': GooglePlayRetriever()
        }
        self.analyzers = {
            'screenshot': ScreenshotAnalyzer(),
            'icon': IconAnalyzer(),
            'feature_graphic': FeatureGraphicAnalyzer()
        }
        self.scorer = CreativeScorer()
    
    def fetch_and_analyze_assets(self, app_id: str, platform: str) -> Dict[str, Any]:
        """Fetch and analyze creative assets for an app"""
        # Get retriever
        retriever = self.retrievers.get(platform)
        if not retriever:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Fetch assets
        assets = retriever.retrieve_assets(app_id)
        
        # Analyze each asset
        analyzed_assets = {}
        for asset_type, asset_data in assets.items():
            if asset_data is None:
                continue
            
            # Get analyzer
            analyzer = self.analyzers.get(asset_type, None)
            
            if analyzer:
                analysis = analyzer.analyze(asset_data)
                
                # Save asset
                asset = CreativeAsset(
                    id=uuid.uuid4(),
                    app_id=app_id,
                    asset_type=asset_type,
                    asset_url=asset_data.get('url'),
                    width=asset_data.get('width'),
                    height=asset_data.get('height'),
                    aspect_ratio=asset_data.get('width') / asset_data.get('height') if asset_data.get('height') else None,
                    format=asset_data.get('format'),
                    order=asset_data.get('order'),
                    is_published=True,
                    analysis_score=analysis.get('score', 0),
                    analysis_data=analysis,
                    last_analyzed=datetime.utcnow()
                )
                
                self.db.add(asset)
                
                # Save analysis
                analysis_record = CreativeAnalysis(
                    id=uuid.uuid4(),
                    asset_id=asset.id,
                    analysis_type=asset_type,
                    score=analysis.get('score', 0),
                    findings=analysis.get('findings', []),
                    recommendations=self._generate_recommendations(analysis.get('findings', [])),
                    metrics=analysis.get('metrics', {}),
                    analysis_date=datetime.utcnow()
                )
                
                self.db.add(analysis_record)
                
                analyzed_assets[asset_type] = {
                    'id': str(asset.id),
                    'url': asset.asset_url,
                    'score': asset.analysis_score,
                    'analysis': analysis
                }
        
        self.db.commit()
        
        # Calculate overall score
        scores = [a.get('score', 0) for a in analyzed_assets.values()]
        overall_score = self.scorer.calculate_overall_score(scores)
        
        return {
            'assets': analyzed_assets,
            'overall_score': overall_score,
            'asset_count': len(analyzed_assets)
        }
    
    def get_assets(self, app_id: str) -> Dict[str, Any]:
        """Get all creative assets for an app"""
        assets = self.db.query(CreativeAsset).filter(
            CreativeAsset.app_id == app_id,
            CreativeAsset.is_published == True
        ).order_by(CreativeAsset.asset_type, CreativeAsset.order).all()
        
        grouped = {}
        for asset in assets:
            if asset.asset_type not in grouped:
                grouped[asset.asset_type] = []
            grouped[asset.asset_type].append({
                'id': str(asset.id),
                'url': asset.asset_url,
                'score': asset.analysis_score,
                'width': asset.width,
                'height': asset.height,
                'order': asset.order,
                'format': asset.format,
                'last_analyzed': asset.last_analyzed.isoformat() if asset.last_analyzed else None
            })
        
        return grouped
    
    def get_asset_history(self, app_id: str) -> List[Dict]:
        """Get creative history for an app"""
        history = self.db.query(CreativeHistory).filter(
            CreativeHistory.app_id == app_id
        ).order_by(CreativeHistory.detected_date.desc()).limit(50).all()
        
        return [{
            'id': str(h.id),
            'asset_type': h.asset_type,
            'change_type': h.change_type,
            'summary': h.change_summary,
            'date': h.detected_date.isoformat()
        } for h in history]
    
    def get_creative_dashboard(self, app_id: str) -> Dict[str, Any]:
        """Get creative dashboard data"""
        assets = self.db.query(CreativeAsset).filter(
            CreativeAsset.app_id == app_id,
            CreativeAsset.is_published == True
        ).all()
        
        if not assets:
            return {
                'overall_score': 0,
                'asset_count': 0,
                'scores': {},
                'quick_wins': []
            }
        
        scores = {a.asset_type: a.analysis_score for a in assets if a.analysis_score}
        overall_score = self.scorer.calculate_overall_score(list(scores.values()))
        
        # Find quick wins (lowest scores)
        quick_wins = sorted(
            [{'type': a.asset_type, 'score': a.analysis_score, 'id': str(a.id)} for a in assets if a.analysis_score],
            key=lambda x: x['score']
        )[:3]
        
        return {
            'overall_score': overall_score,
            'asset_count': len(assets),
            'scores': scores,
            'quick_wins': quick_wins
        }
    
    def _generate_recommendations(self, findings: List[Dict]) -> List[Dict]:
        """Generate recommendations from findings"""
        recommendations = []
        
        for finding in findings:
            if finding.get('recommendation'):
                recommendations.append({
                    'text': finding['recommendation'],
                    'impact': self._estimate_impact(finding),
                    'effort': self._estimate_effort(finding)
                })
        
        return recommendations
    
    def _estimate_impact(self, finding: Dict) -> str:
        impact_map = {
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        return impact_map.get(finding.get('impact', 'medium'), 'medium')
    
    def _estimate_effort(self, finding: Dict) -> str:
        # Estimate effort based on finding type
        if 'screenshot' in finding.get('recommendation', '').lower():
            return 'medium'
        elif 'icon' in finding.get('recommendation', '').lower():
            return 'medium'
        else:
            return 'low'
