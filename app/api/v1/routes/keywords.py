from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.keyword_service import KeywordService

router = APIRouter(prefix="/keywords", tags=["Keywords"])


@router.post("/{app_id}/track")
async def track_keyword(
    app_id: str,
    keyword_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start tracking a keyword for an app"""
    service = KeywordService(db)
    result = service.track_keyword(app_id, keyword_id)
    return result


@router.post("/{app_id}/untrack")
async def untrack_keyword(
    app_id: str,
    keyword_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Stop tracking a keyword"""
    service = KeywordService(db)
    result = service.untrack_keyword(app_id, keyword_id)
    return result


@router.get("/{app_id}/opportunities")
async def get_opportunities(
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get keyword opportunities for an app"""
    service = KeywordService(db)
    return service.get_opportunities(app_id)


@router.get("/{app_id}/competitors/{competitor_id}")
async def get_competitor_keywords(
    app_id: str,
    competitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get competitor keywords comparison"""
    service = KeywordService(db)
    return service.get_competitor_keywords(app_id, competitor_id)
