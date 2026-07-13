from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/pricing", tags=["Pricing"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def pricing_page(request: Request):
    """Render the pricing page"""
    return templates.TemplateResponse(
        "pricing/index.html",
        {"request": request}
    )
