from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="Novexium", version="1.0.0")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# THIS IS THE CRITICAL ROUTE YOU'RE MISSING:
@app.get("/")
async def root():
    return {"message": "Novexium API is running!"}

# Also add a health check
@app.get("/health")
async def health():
    return {"status": "healthy"}
