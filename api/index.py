import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import the app
try:
    from app.main import app
    print("✅ App imported successfully")
except Exception as e:
    print(f"❌ Error: {e}")
    # Fallback to a minimal app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Novexium API (fallback)"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}

# Vercel expects a 'handler'
handler = app
