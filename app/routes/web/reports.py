from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def report_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the report dashboard"""
    service = ReportService(db)
    reports = service.get_reports(str(current_user.id))
    templates = service.get_templates(str(current_user.id))
    
    return templates.TemplateResponse(
        "reports/index.html",
        {
            "request": request,
            "reports": reports,
            "templates": templates
        }
    )


@router.get("/builder", response_class=HTMLResponse)
async def report_builder(
    request: Request,
    template_id: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the report builder"""
    service = ReportService(db)
    
    template = None
    if template_id:
        templates = service.get_templates(str(current_user.id))
        template = next((t for t in templates if t['id'] == template_id), None)
    
    return templates.TemplateResponse(
        "reports/builder.html",
        {
            "request": request,
            "template": template
        }
    )


@router.get("/schedules", response_class=HTMLResponse)
async def report_schedules(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the report schedules page"""
    return templates.TemplateResponse(
        "reports/schedules.html",
        {"request": request}
    )
