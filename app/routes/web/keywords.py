from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.keyword_service import KeywordService

router = APIRouter(prefix="/apps/{app_id}/keywords", tags=["Keywords"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def keyword_dashboard(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the keyword dashboard"""
    service = KeywordService(db)
    dashboard = service.get_keyword_dashboard(app_id)
    
    return templates.TemplateResponse(
        "keywords/index.html",
        {
            "request": request,
            "app_id": app_id,
            "dashboard": dashboard
        }
    )


@router.get("/explorer", response_class=HTMLResponse)
async def keyword_explorer(
    request: Request,
    app_id: str,
    q: str = Query("", description="Search query"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the keyword explorer"""
    service = KeywordService(db)
    keywords = service.search_keywords(q, app_id) if q else []
    
    return templates.TemplateResponse(
        "keywords/explorer.html",
        {
            "request": request,
            "app_id": app_id,
            "keywords": keywords,
            "query": q
        }
    )


@router.get("/opportunities", response_class=HTMLResponse)
async def keyword_opportunities(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the keyword opportunities page"""
    service = KeywordService(db)
    opportunities = service.get_opportunities(app_id)
    
    return templates.TemplateResponse(
        "keywords/opportunities.html",
        {
            "request": request,
            "app_id": app_id,
            "opportunities": opportunities
        }
    )


@router.get("/history", response_class=HTMLResponse)
async def keyword_history(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the keyword history page"""
    return templates.TemplateResponse(
        "keywords/history.html",
        {
            "request": request,
            "app_id": app_id
        }
    )
