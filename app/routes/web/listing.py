from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.listing_service import ListingService

router = APIRouter(prefix="/apps/{app_id}/listing", tags=["Store Listing"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def listing_workspace(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the store listing workspace"""
    service = ListingService(db)
    listing = service.get_listing(app_id)
    draft = service.get_draft(listing['id']) if listing else None
    
    return templates.TemplateResponse(
        "listing/index.html",
        {
            "request": request,
            "app_id": app_id,
            "listing": listing,
            "draft": draft
        }
    )


@router.get("/history", response_class=HTMLResponse)
async def listing_history(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the version history page"""
    service = ListingService(db)
    listing = service.get_listing(app_id)
    versions = service.get_versions(listing['id']) if listing else []
    
    return templates.TemplateResponse(
        "listing/history.html",
        {
            "request": request,
            "app_id": app_id,
            "versions": versions
        }
    )
