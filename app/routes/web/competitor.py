from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.competitor_service import CompetitorService

router = APIRouter(prefix="/apps/{app_id}/competitors", tags=["Competitors"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def competitor_dashboard(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the competitor dashboard"""
    service = CompetitorService(db)
    competitors = service.get_competitors(app_id)
    changes = service.get_changes(app_id, 7)
    insights = service.get_insights(app_id)
    
    return templates.TemplateResponse(
        "competitor/index.html",
        {
            "request": request,
            "app_id": app_id,
            "competitors": competitors,
            "changes": changes,
            "insights": insights
        }
    )


@router.get("/{competitor_id}", response_class=HTMLResponse)
async def competitor_detail(
    request: Request,
    app_id: str,
    competitor_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render competitor detail page"""
    service = CompetitorService(db)
    detail = service.get_competitor_detail(competitor_id)
    
    return templates.TemplateResponse(
        "competitor/detail.html",
        {
            "request": request,
            "app_id": app_id,
            "detail": detail
        }
    )


@router.get("/comparison", response_class=HTMLResponse)
async def competitor_comparison(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render competitor comparison page"""
    return templates.TemplateResponse(
        "competitor/comparison.html",
        {
            "request": request,
            "app_id": app_id
        }
    )
