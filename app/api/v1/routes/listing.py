from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.listing_service import ListingService

router = APIRouter(prefix="/listing", tags=["Store Listing"])


@router.post("/update")
async def update_listing(
    data: Dict[str, Any],
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the store listing"""
    service = ListingService(db)
    return service.create_or_update_listing(app_id, data, str(current_user.id))


@router.post("/draft")
async def save_draft(
    data: Dict[str, Any],
    listing_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save a draft"""
    service = ListingService(db)
    return service.save_draft(listing_id, data, str(current_user.id))


@router.get("/{listing_id}/versions")
async def get_versions(
    listing_id: str,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get version history"""
    service = ListingService(db)
    return service.get_versions(listing_id, limit)


@router.get("/versions/compare/{v1_id}/{v2_id}")
async def compare_versions(
    v1_id: str,
    v2_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two versions"""
    service = ListingService(db)
    return service.compare_versions(v1_id, v2_id)


@router.post("/versions/{version_id}/restore")
async def restore_version(
    version_id: str,
    listing_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Restore a version"""
    service = ListingService(db)
    return service.restore_version(version_id, listing_id)
