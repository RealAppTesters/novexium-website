from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.store_listing import StoreListing
from app.models.listing_version import ListingVersion
from app.models.listing_draft import ListingDraft
from app.store_listing.scoring.title import TitleScorer
from app.store_listing.scoring.description import DescriptionScorer
from app.store_listing.scoring.completeness import CompletenessScorer
from app.store_listing.scoring.readability import ReadabilityScorer
from app.store_listing.recommendations.generator import ListingRecommendationGenerator


class ListingService:
    def __init__(self, db: Session):
        self.db = db
        self.title_scorer = TitleScorer()
        self.description_scorer = DescriptionScorer()
        self.completeness_scorer = CompletenessScorer()
        self.readability_scorer = ReadabilityScorer()
        self.recommendation_generator = ListingRecommendationGenerator()
    
    def get_listing(self, app_id: str) -> Optional[Dict]:
        """Get the store listing for an app"""
        listing = self.db.query(StoreListing).filter(
            StoreListing.app_id == app_id,
            StoreListing.is_active == True
        ).first()
        
        if not listing:
            return None
        
        return self._listing_to_dict(listing)
    
    def create_or_update_listing(self, app_id: str, data: Dict, user_id: str) -> Dict:
        """Create or update a store listing"""
        listing = self.db.query(StoreListing).filter(
            StoreListing.app_id == app_id,
            StoreListing.is_active == True
        ).first()
        
        if not listing:
            listing = StoreListing(
                id=uuid.uuid4(),
                app_id=app_id,
                platform=data.get('platform', 'app_store'),
                title=data.get('title', ''),
                short_description=data.get('short_description', ''),
                long_description=data.get('long_description', ''),
                promotional_text=data.get('promotional_text', ''),
                what_new=data.get('what_new', ''),
                release_notes=data.get('release_notes', ''),
                language=data.get('language', 'en'),
                localization_country=data.get('localization_country', 'US')
            )
            self.db.add(listing)
        else:
            # Save current version before updating
            self._save_version(listing, user_id, "Auto-saved before update")
            
            # Update listing
            listing.title = data.get('title', listing.title)
            listing.short_description = data.get('short_description', listing.short_description)
            listing.long_description = data.get('long_description', listing.long_description)
            listing.promotional_text = data.get('promotional_text', listing.promotional_text)
            listing.what_new = data.get('what_new', listing.what_new)
            listing.release_notes = data.get('release_notes', listing.release_notes)
            listing.language = data.get('language', listing.language)
            listing.localization_country = data.get('localization_country', listing.localization_country)
        
        # Calculate scores
        listing.title_score = self.title_scorer.score(listing.title, listing.platform)
        listing.description_score = self.description_scorer.score(
            listing.short_description or '',
            listing.long_description or ''
        )
        listing.readability_score = self.readability_scorer.score(
            listing.long_description or ''
        )
        listing.completeness_score = self.completeness_scorer.score(listing)
        listing.keyword_coverage_score = self._calculate_keyword_coverage(listing)
        
        # Calculate overall score
        listing.optimization_score = self._calculate_overall_score(listing)
        listing.last_optimized = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(listing)
        
        return self._listing_to_dict(listing)
    
    def get_draft(self, listing_id: str) -> Optional[Dict]:
        """Get the current draft for a listing"""
        draft = self.db.query(ListingDraft).filter(
            ListingDraft.listing_id == listing_id,
            ListingDraft.is_autosave == True
        ).order_by(ListingDraft.last_autosave.desc()).first()
        
        if not draft:
            return None
        
        return self._draft_to_dict(draft)
    
    def save_draft(self, listing_id: str, data: Dict, user_id: str) -> Dict:
        """Save a draft"""
        draft = ListingDraft(
            id=uuid.uuid4(),
            listing_id=listing_id,
            title=data.get('title'),
            short_description=data.get('short_description'),
            long_description=data.get('long_description'),
            promotional_text=data.get('promotional_text'),
            what_new=data.get('what_new'),
            release_notes=data.get('release_notes'),
            draft_name=data.get('draft_name', 'Auto-saved draft'),
            last_autosave=datetime.utcnow(),
            is_autosave=True
        )
        
        self.db.add(draft)
        self.db.commit()
        
        return self._draft_to_dict(draft)
    
    def get_versions(self, listing_id: str, limit: int = 20) -> List[Dict]:
        """Get version history for a listing"""
        versions = self.db.query(ListingVersion).filter(
            ListingVersion.listing_id == listing_id
        ).order_by(ListingVersion.version_number.desc()).limit(limit).all()
        
        return [self._version_to_dict(v) for v in versions]
    
    def compare_versions(self, version1_id: str, version2_id: str) -> Dict:
        """Compare two versions"""
        v1 = self.db.query(ListingVersion).filter(ListingVersion.id == version1_id).first()
        v2 = self.db.query(ListingVersion).filter(ListingVersion.id == version2_id).first()
        
        if not v1 or not v2:
            return None
        
        return {
            'version1': {
                'id': str(v1.id),
                'name': v1.version_name or f'Version {v1.version_number}',
                'score': v1.optimization_score,
                'date': v1.created_at.isoformat()
            },
            'version2': {
                'id': str(v2.id),
                'name': v2.version_name or f'Version {v2.version_number}',
                'score': v2.optimization_score,
                'date': v2.created_at.isoformat()
            },
            'changes': {
                'title': self._compare_text(v1.title, v2.title),
                'short_description': self._compare_text(v1.short_description, v2.short_description),
                'long_description': self._compare_text(v1.long_description, v2.long_description),
                'score_change': v2.optimization_score - v1.optimization_score
            }
        }
    
    def restore_version(self, version_id: str, listing_id: str) -> Dict:
        """Restore a version"""
        version = self.db.query(ListingVersion).filter(ListingVersion.id == version_id).first()
        
        if not version:
            return None
        
        listing = self.db.query(StoreListing).filter(StoreListing.id == listing_id).first()
        if not listing:
            return None
        
        # Save current version
        self._save_version(listing, "System", f"Before restoring version {version.version_number}")
        
        # Restore
        listing.title = version.title
        listing.short_description = version.short_description
        listing.long_description = version.long_description
        listing.promotional_text = version.promotional_text
        listing.what_new = version.what_new
        listing.release_notes = version.release_notes
        
        # Recalculate scores
        listing.optimization_score = version.optimization_score
        listing.last_optimized = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(listing)
        
        return self._listing_to_dict(listing)
    
    def _listing_to_dict(self, listing: StoreListing) -> Dict:
        return {
            'id': str(listing.id),
            'app_id': str(listing.app_id),
            'platform': listing.platform,
            'title': listing.title,
            'short_description': listing.short_description,
            'long_description': listing.long_description,
            'promotional_text': listing.promotional_text,
            'what_new': listing.what_new,
            'release_notes': listing.release_notes,
            'language': listing.language,
            'localization_country': listing.localization_country,
            'optimization_score': listing.optimization_score,
            'title_score': listing.title_score,
            'description_score': listing.description_score,
            'readability_score': listing.readability_score,
            'keyword_coverage_score': listing.keyword_coverage_score,
            'completeness_score': listing.completeness_score,
            'last_optimized': listing.last_optimized.isoformat() if listing.last_optimized else None
        }
    
    def _draft_to_dict(self, draft: ListingDraft) -> Dict:
        return {
            'id': str(draft.id),
            'title': draft.title,
            'short_description': draft.short_description,
            'long_description': draft.long_description,
            'promotional_text': draft.promotional_text,
            'what_new': draft.what_new,
            'release_notes': draft.release_notes,
            'draft_name': draft.draft_name,
            'last_autosave': draft.last_autosave.isoformat() if draft.last_autosave else None
        }
    
    def _version_to_dict(self, version: ListingVersion) -> Dict:
        return {
            'id': str(version.id),
            'version_number': version.version_number,
            'version_name': version.version_name,
            'change_summary': version.change_summary,
            'optimization_score': version.optimization_score,
            'created_at': version.created_at.isoformat(),
            'created_by': str(version.created_by)
        }
    
    def _save_version(self, listing: StoreListing, user_id: str, summary: str = None):
        """Save a version before making changes"""
        version_number = self.db.query(ListingVersion).filter(
            ListingVersion.listing_id == listing.id
        ).count() + 1
        
        version = ListingVersion(
            id=uuid.uuid4(),
            listing_id=listing.id,
            title=listing.title,
            short_description=listing.short_description,
            long_description=listing.long_description,
            promotional_text=listing.promotional_text,
            what_new=listing.what_new,
            release_notes=listing.release_notes,
            version_number=version_number,
            change_summary=summary or f"Version {version_number}",
            optimization_score=listing.optimization_score,
            created_by=user_id
        )
        
        self.db.add(version)
        self.db.commit()
    
    def _calculate_overall_score(self, listing: StoreListing) -> int:
        """Calculate overall optimization score"""
        weights = {
            'title': 0.25,
            'description': 0.25,
            'readability': 0.15,
            'keyword_coverage': 0.20,
            'completeness': 0.15
        }
        
        score = (
            listing.title_score * weights['title'] +
            listing.description_score * weights['description'] +
            listing.readability_score * weights['readability'] +
            listing.keyword_coverage_score * weights['keyword_coverage'] +
            listing.completeness_score * weights['completeness']
        )
        
        return int(round(score))
    
    def _calculate_keyword_coverage(self, listing: StoreListing) -> int:
        """Calculate keyword coverage score"""
        # Mock implementation
        return 75
    
    def _compare_text(self, text1: str, text2: str) -> Dict:
        """Compare two text strings"""
        return {
            'changed': text1 != text2,
            'length_change': len(text2 or '') - len(text1 or '')
        }
