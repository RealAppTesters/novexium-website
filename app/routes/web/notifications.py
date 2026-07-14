from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def notification_center(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the notification center"""
    service = NotificationService(db)
    notifications = service.get_notifications(str(current_user.id), limit=50)
    unread_count = service.get_unread_count(str(current_user.id))
    
    return templates.TemplateResponse(
        "notifications/index.html",
        {
            "request": request,
            "notifications": notifications,
            "unread_count": unread_count
        }
    )


@router.get("/activity", response_class=HTMLResponse)
async def activity_timeline(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the activity timeline"""
    service = NotificationService(db)
    activities = service.get_activity(str(current_user.id), limit=100)
    
    return templates.TemplateResponse(
        "notifications/activity.html",
        {
            "request": request,
            "activities": activities
        }
    )


@router.get("/summary", response_class=HTMLResponse)
async def notification_summary(
    request: Request,
    period: str = Query("daily"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the summary page"""
    service = NotificationService(db)
    summary = service.generate_summary(str(current_user.id), period)
    
    return templates.TemplateResponse(
        "notifications/summary.html",
        {
            "request": request,
            "summary": summary,
            "period": period
        }
    )
