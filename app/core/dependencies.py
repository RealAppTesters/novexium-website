from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database.session import get_db
from app.models.user import User
from app.models.session import Session as UserSession
from app.services.auth_service import AuthService
from app.core.config import settings

security = HTTPBearer()

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    optional: bool = False
) -> Optional[User]:
    """Get the current authenticated user from session cookie"""
    token = request.cookies.get("session_token")
    
    if not token:
        if optional:
            return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    auth_service = AuthService(db)
    session = auth_service.get_session(token)
    
    if not session:
        if optional:
            return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    user = db.query(User).filter(User.id == session.user_id).first()
    
    if not user:
        if optional:
            return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Check if user is active
    if user.deleted_at is not None:
        if optional:
            return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account deactivated"
        )
    
    return user

async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user or None if not authenticated"""
    return await get_current_user(request, db, optional=True)

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current user (must be active)"""
    if current_user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account deactivated"
        )
    return current_user

async def get_current_user_id(
    current_user: User = Depends(get_current_active_user)
) -> UUID:
    """Get current user ID"""
    return current_user.id
