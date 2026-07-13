from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/solutions", tags=["Solutions"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def solutions_page(request: Request):
    """Render the solutions page"""
    return templates.TemplateResponse(
        "solutions/index.html",
        {"request": request}
    )
