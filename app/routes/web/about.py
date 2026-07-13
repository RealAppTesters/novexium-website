from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/about", tags=["About"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def about_page(request: Request):
    """Render the about page"""
    return templates.TemplateResponse(
        "about/index.html",
        {"request": request}
    )
