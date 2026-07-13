from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from typing import List
from app.services.auth_service import AuthService
from app.database.session import SessionLocal

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to check authentication for protected routes"""
    
    PUBLIC_PATHS = [
        "/",
        "/auth/login",
        "/auth/register",
        "/auth/forgot-password",
        "/auth/reset-password",
        "/auth/verify",
        "/auth/verify-email-sent",
        "/auth/verify-success",
        "/auth/verify-error",
        "/static",
        "/favicon.ico"
    ]
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Skip auth check for public paths
        if any(path.startswith(p) for p in self.PUBLIC_PATHS):
            return await call_next(request)
        
        # Check for session token
        token = request.cookies.get("session_token")
        
        if token:
            # Validate session
            db = SessionLocal()
            try:
                auth_service = AuthService(db)
                session = auth_service.get_session(token)
                if session:
                    # Set user in request state
                    request.state.user_id = session.user_id
                    return await call_next(request)
            finally:
                db.close()
        
        # Not authenticated - redirect to login
        return RedirectResponse(
            url="/auth/login",
            status_code=status.HTTP_302_FOUND
        )
