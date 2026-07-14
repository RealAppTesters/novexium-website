from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.creative_service import CreativeService

router = APIRouter(prefix="/apps/{app_id}/creative", tags=["Creative Studio"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def creative_studio(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the creative studio"""
    service = CreativeService(db)
    dashboard = service.get_creative_dashboard(app_id)
    assets = service.get_assets(app_id)
    history = service.get_asset_history(app_id)
    
    return templates.TemplateResponse(
        "creative/index.html",
        {
            "request": request,
            "app_id": app_id,
            "dashboard": dashboard,
            "assets": assets,
            "history": history
        }
    )


@router.get("/analysis", response_class=HTMLResponse)
async def creative_analysis(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the creative analysis page"""
    service = CreativeService(db)
    assets = service.get_assets(app_id)
    
    return templates.TemplateResponse(
        "creative/analysis.html",
        {
            "request": request,
            "app_id": app_id,
            "assets": assets
        }
    )


@router.get("/comparison", response_class=HTMLResponse)
async def creative_comparison(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the creative comparison page"""
    return templates.TemplateResponse(
        "creative/comparison.html",
        {
            "request": request,
            "app_id": app_id
        }
    )


@router.get("/history", response_class=HTMLResponse)
async def creative_history(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the creative history page"""
    service = CreativeService(db)
    history = service.get_asset_history(app_id)
    
    return templates.TemplateResponse(
        "creative/history.html",
        {
            "request": request,
            "app_id": app_id,
            "history": history
        }
    )
