from app.main import app
print("✅ App loaded successfully")
print(f"Routes: {[route.path for route in app.routes]}")
