from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/resources", tags=["Resources"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def resources_page(request: Request):
    """Render the resources center page"""
    return templates.TemplateResponse(
        "resources/index.html",
        {"request": request}
    )
