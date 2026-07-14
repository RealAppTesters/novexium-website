from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.review_service import ReviewService

router = APIRouter(prefix="/apps/{app_id}/reviews", tags=["Reviews"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def review_dashboard(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the review dashboard"""
    service = ReviewService(db)
    dashboard = service.get_dashboard(app_id)
    
    return templates.TemplateResponse(
        "reviews/index.html",
        {
            "request": request,
            "app_id": app_id,
            "dashboard": dashboard
        }
    )


@router.get("/feed", response_class=HTMLResponse)
async def review_feed(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the review feed"""
    service = ReviewService(db)
    reviews = service.get_reviews(app_id, limit=50)
    
    return templates.TemplateResponse(
        "reviews/feed.html",
        {
            "request": request,
            "app_id": app_id,
            "reviews": reviews
        }
    )


@router.get("/analysis", response_class=HTMLResponse)
async def review_analysis(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the review analysis page"""
    service = ReviewService(db)
    insights = service.generate_insights(app_id)
    dashboard = service.get_dashboard(app_id)
    
    return templates.TemplateResponse(
        "reviews/analysis.html",
        {
            "request": request,
            "app_id": app_id,
            "insights": insights,
            "dashboard": dashboard
        }
    )
