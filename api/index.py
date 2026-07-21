import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app
from app.main import app

# Vercel needs 'app' at the top level
# The import above gives us 'app', so we're done!

# If you need a fallback, define it directly in this file
# but the import should work if your app/main.py is correct
