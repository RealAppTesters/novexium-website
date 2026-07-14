from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.rank_service import RankService

router = APIRouter(prefix="/apps/{app_id}/rank", tags=["Rank Tracking"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def rank_dashboard(
    request: Request,
    app_id: str,
    country: str = Query("US", description="Country code"),
    language: str = Query("en", description="Language code"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the rank tracking dashboard"""
    service = RankService(db)
    rankings = service.get_rankings(app_id, country, language)
    visibility = service.get_visibility(app_id, country, language)
    alerts = service.get_alerts(app_id, 10)
    
    return templates.TemplateResponse(
        "rank/index.html",
        {
            "request": request,
            "app_id": app_id,
            "rankings": rankings,
            "visibility": visibility,
            "alerts": alerts,
            "country": country,
            "language": language
        }
    )


@router.get("/history", response_class=HTMLResponse)
async def rank_history(
    request: Request,
    app_id: str,
    country: str = Query("US"),
    language: str = Query("en"),
    keyword: str = Query(""),
    days: int = Query(30),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the rank history page"""
    service = RankService(db)
    history = service.get_rank_history(app_id, keyword, country, language, days) if keyword else []
    
    return templates.TemplateResponse(
        "rank/history.html",
        {
            "request": request,
            "app_id": app_id,
            "history": history,
            "keyword": keyword,
            "country": country,
            "language": language,
            "days": days
        }
    )
