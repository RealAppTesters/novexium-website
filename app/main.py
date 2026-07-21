from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="Novexium", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ============================================
# API ROUTES (JSON Responses)
# ============================================

@app.get("/api")
async def api_root():
    return {
        "message": "Novexium API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": [
            "/",
            "/api",
            "/api/health",
            "/auth/login",
            "/auth/register",
            "/dashboard",
            "/apps",
            "/pricing",
            "/platform",
            "/solutions",
            "/resources",
            "/about",
            "/contact"
        ]
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat()}

# ============================================
# PUBLIC WEB ROUTES (HTML Pages)
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Homepage - Conversion-focused landing page"""
    return templates.TemplateResponse(
        "public/index.html",
        {"request": request}
    )

@app.get("/platform", response_class=HTMLResponse)
async def platform_page(request: Request):
    """Platform page - Product tour"""
    return templates.TemplateResponse(
        "platform/index.html",
        {"request": request}
    )

@app.get("/solutions", response_class=HTMLResponse)
async def solutions_page(request: Request):
    """Solutions page - For different audiences"""
    return templates.TemplateResponse(
        "solutions/index.html",
        {"request": request}
    )

@app.get("/pricing", response_class=HTMLResponse)
async def pricing_page(request: Request):
    """Pricing page - Plans and subscription"""
    return templates.TemplateResponse(
        "pricing/index.html",
        {"request": request}
    )

@app.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    """Resources Center - Guides and downloads"""
    return templates.TemplateResponse(
        "resources/index.html",
        {"request": request}
    )

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page - Company information"""
    return templates.TemplateResponse(
        "about/index.html",
        {"request": request}
    )

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page - Get in touch"""
    return templates.TemplateResponse(
        "contact/index.html",
        {"request": request}
    )

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request}
    )

@app.get("/auth/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page"""
    return templates.TemplateResponse(
        "auth/register.html",
        {"request": request}
    )

@app.get("/auth/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Forgot password page"""
    return templates.TemplateResponse(
        "auth/forgot_password.html",
        {"request": request}
    )

@app.get("/auth/verify/{token}", response_class=HTMLResponse)
async def verify_email_page(request: Request, token: str):
    """Email verification page"""
    return templates.TemplateResponse(
        "auth/verify_email.html",
        {"request": request, "token": token}
    )

# ============================================
# DASHBOARD ROUTES (Protected - Add auth later)
# ============================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """User Dashboard"""
    return templates.TemplateResponse(
        "dashboard/index.html",
        {"request": request}
    )

@app.get("/apps", response_class=HTMLResponse)
async def apps_page(request: Request):
    """My Apps page"""
    return templates.TemplateResponse(
        "apps/index.html",
        {"request": request}
    )

@app.get("/apps/{app_id}/workspace", response_class=HTMLResponse)
async def app_workspace(request: Request, app_id: str):
    """App Workspace"""
    return templates.TemplateResponse(
        "apps/workspace.html",
        {"request": request, "app_id": app_id}
    )

# ============================================
# ERROR HANDLING
# ============================================

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse(
        "errors/404.html",
        {"request": request},
        status_code=404
    )

@app.exception_handler(500)
async def server_error(request: Request, exc):
    return templates.TemplateResponse(
        "errors/500.html",
        {"request": request},
        status_code=500
    )

# ============================================
# If you have route modules, import them here:
# ============================================

# from app.routes.web import auth
# app.include_router(auth.router)

# from app.api.v1.routes import auth as api_auth
# app.include_router(api_auth.router, prefix="/api/v1")
