from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/contact", tags=["Contact"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Render the contact page"""
    return templates.TemplateResponse(
        "contact/index.html",
        {"request": request}
    )
