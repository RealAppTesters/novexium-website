from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.middleware.auth import AuthMiddleware
from app.routes.web import auth
from app.core.config import settings

app = FastAPI(title="Novexium", version="1.0.0")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Add auth middleware
app.add_middleware(AuthMiddleware)

# Include auth routes
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Novexium API"}

@app.get("/dashboard")
async def dashboard():
    # Will be implemented in Badge 07
    return {"message": "Dashboard coming soon"}
