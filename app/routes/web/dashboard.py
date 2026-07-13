from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.app import App

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the main dashboard"""
    
    # Get user's apps
    apps = db.query(App).filter(App.user_id == current_user.id).all()
    app_count = len(apps)
    
    # Calculate time of day
    hour = datetime.now().hour
    if hour < 12:
        time_of_day = "Morning"
    elif hour < 17:
        time_of_day = "Afternoon"
    else:
        time_of_day = "Evening"
    
    # Calculate trial days left
    trial_days_left = 0
    if current_user.trial_end:
        trial_days_left = (current_user.trial_end - datetime.utcnow()).days
        trial_days_left = max(0, trial_days_left)
    
    # If no apps, show empty state
    if app_count == 0:
        return templates.TemplateResponse(
            "dashboard/empty_state.html",
            {
                "request": request,
                "user": current_user,
                "time_of_day": time_of_day,
                "current_date": datetime.now().strftime("%B %d, %Y"),
                "app_count": app_count,
                "trial_days_left": trial_days_left
            }
        )
    
    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "user": current_user,
            "time_of_day": time_of_day,
            "current_date": datetime.now().strftime("%B %d, %Y"),
            "app_count": app_count,
            "trial_days_left": trial_days_left,
            "apps": apps
        }
    )
