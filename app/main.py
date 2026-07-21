from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import os

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

# Add custom functions to template context
def get_flashed_messages():
    """Mock flash messages for templates - replace with real implementation later"""
    return []

# Add the function to template globals
templates.env.globals['get_flashed_messages'] = get_flashed_messages

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ============================================
# API ROUTES
# ============================================

@app.get("/api")
async def api_root():
    return {
        "message": "Novexium API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# ============================================
# WEB ROUTES WITH ERROR HANDLING
# ============================================

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    try:
        return templates.TemplateResponse("public/index.html", {"request": request})
    except Exception as e:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>Novexium</title></head>
        <body>
            <h1>Novexium</h1>
            <p>Welcome to Novexium! (Template not found, using fallback)</p>
            <p>Error: {str(e)}</p>
        </body>
        </html>
        """)

@app.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    try:
        return templates.TemplateResponse("auth/login.html", {"request": request})
    except Exception:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Login - Novexium</title></head>
        <body>
            <h1>Log In</h1>
            <form>
                <input type="email" placeholder="Email"><br>
                <input type="password" placeholder="Password"><br>
                <button>Log In</button>
            </form>
            <a href="/auth/register">Sign up</a>
        </body>
        </html>
        """)

@app.get("/auth/register", response_class=HTMLResponse)
async def register_page(request: Request):
    try:
        return templates.TemplateResponse("auth/register.html", {"request": request})
    except Exception:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Register - Novexium</title></head>
        <body>
            <h1>Create Account</h1>
            <form>
                <input type="text" placeholder="Full Name"><br>
                <input type="email" placeholder="Email"><br>
                <input type="password" placeholder="Password"><br>
                <button>Create Account</button>
            </form>
            <a href="/auth/login">Log in</a>
        </body>
        </html>
        """)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    try:
        return templates.TemplateResponse("dashboard/index.html", {"request": request})
    except Exception:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Dashboard - Novexium</title></head>
        <body>
            <h1>Dashboard</h1>
            <p>Welcome to your Novexium dashboard!</p>
            <a href="/">Home</a>
        </body>
        </html>
        """)

@app.get("/pricing", response_class=HTMLResponse)
async def pricing_page(request: Request):
    try:
        return templates.TemplateResponse("pricing/index.html", {"request": request})
    except Exception:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Pricing - Novexium</title></head>
        <body>
            <h1>Simple Pricing</h1>
            <div>
                <h3>Starter - $15/mo</h3>
                <h3>Professional - $39/mo</h3>
                <h3>Agency - $99/mo</h3>
            </div>
        </body>
        </html>
        """)

# ============================================
# ERROR HANDLING
# ============================================

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body>
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/">Return Home</a>
    </body>
    </html>
    """, status_code=404)

@app.exception_handler(500)
async def server_error(request: Request, exc):
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>500 - Server Error</title></head>
    <body>
        <h1>500 - Server Error</h1>
        <p>Something went wrong. We're working on it.</p>
        <a href="/">Return Home</a>
    </body>
    </html>
    """, status_code=500)
