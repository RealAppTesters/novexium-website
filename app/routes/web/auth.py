from fastapi import APIRouter, Request, Form, HTTPException, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database.session import get_db
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")

# ============================================
# REGISTER
# ============================================

@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user(optional=True))
):
    """Render the registration page"""
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse(
        "auth/register.html",
        {"request": request}
    )

@router.post("/register")
async def register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    accept_terms: bool = Form(...),
    db: Session = Depends(get_db)
):
    """Handle user registration"""
    # Validate
    if not full_name or len(full_name) < 2:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Please enter your full name",
                "form_data": {"full_name": full_name, "email": email}
            }
        )
    
    if not email or "@" not in email:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Please enter a valid email address",
                "form_data": {"full_name": full_name, "email": email}
            }
        )
    
    if not password or len(password) < 8:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Password must be at least 8 characters",
                "form_data": {"full_name": full_name, "email": email}
            }
        )
    
    if password != confirm_password:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Passwords do not match",
                "form_data": {"full_name": full_name, "email": email}
            }
        )
    
    if not accept_terms:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "You must accept the terms and conditions",
                "form_data": {"full_name": full_name, "email": email}
            }
        )
    
    try:
        # Create user
        auth_service = AuthService(db)
        user = auth_service.create_user(email, full_name, password)
        
        # Send verification email
        email_service = EmailService()
        token = auth_service.generate_email_verification_token(user.id)
        email_service.send_verification_email(email, full_name, token)
        
        # Log user in
        session = auth_service.create_session(user.id)
        
        response = RedirectResponse(
            url="/auth/verify-email-sent",
            status_code=status.HTTP_302_FOUND
        )
        response.set_cookie(
            key="session_token",
            value=session.token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 days
        )
        
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": e.detail,
                "form_data": {"full_name": full_name, "email": email}
            }
        )

# ============================================
# LOGIN
# ============================================

@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user(optional=True))
):
    """Render the login page"""
    if current_user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request}
    )

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Handle user login"""
    if not email or not password:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Please fill in all fields",
                "form_data": {"email": email}
            }
        )
    
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(email, password)
    
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Invalid email or password",
                "form_data": {"email": email}
            }
        )
    
    # Create session
    session = auth_service.create_session(
        user_id=user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        remember_me=remember_me
    )
    
    response = RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(
        key="session_token",
        value=session.token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=30 * 24 * 60 * 60 if remember_me else 7 * 24 * 60 * 60  # 30 or 7 days
    )
    
    return response

# ============================================
# LOGOUT
# ============================================

@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle user logout"""
    token = request.cookies.get("session_token")
    
    if token:
        auth_service = AuthService(db)
        auth_service.delete_session(token)
    
    response = RedirectResponse(
        url="/auth/login",
        status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("session_token")
    
    return response

@router.post("/logout-all")
async def logout_all(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user())
):
    """Logout from all devices"""
    token = request.cookies.get("session_token")
    
    auth_service = AuthService(db)
    count = auth_service.delete_all_sessions(current_user.id, token)
    
    response = RedirectResponse(
        url="/auth/login",
        status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("session_token")
    
    return response

# ============================================
# FORGOT PASSWORD
# ============================================

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Render the forgot password page"""
    return templates.TemplateResponse(
        "auth/forgot_password.html",
        {"request": request}
    )

@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle password reset request"""
    auth_service = AuthService(db)
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Generate reset token
        token = auth_service.generate_password_reset_token(email)
        
        # Send reset email
        email_service = EmailService()
        email_service.send_password_reset_email(email, user.full_name, token)
    
    # Always show success message (security by obscurity)
    return templates.TemplateResponse(
        "auth/forgot_password_sent.html",
        {"request": request, "email": email}
    )

# ============================================
# RESET PASSWORD
# ============================================

@router.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    """Render the reset password page"""
    return templates.TemplateResponse(
        "auth/reset_password.html",
        {"request": request, "token": token}
    )

@router.post("/reset-password/{token}")
async def reset_password(
    request: Request,
    token: str,
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle password reset"""
    if not password or len(password) < 8:
        return templates.TemplateResponse(
            "auth/reset_password.html",
            {
                "request": request,
                "token": token,
                "error": "Password must be at least 8 characters"
            }
        )
    
    if password != confirm_password:
        return templates.TemplateResponse(
            "auth/reset_password.html",
            {
                "request": request,
                "token": token,
                "error": "Passwords do not match"
            }
        )
    
    auth_service = AuthService(db)
    success = auth_service.reset_password(token, password)
    
    if not success:
        return templates.TemplateResponse(
            "auth/reset_password.html",
            {
                "request": request,
                "token": token,
                "error": "Invalid or expired reset link"
            }
        )
    
    return templates.TemplateResponse(
        "auth/reset_password_success.html",
        {"request": request}
    )

# ============================================
# EMAIL VERIFICATION
# ============================================

@router.get("/verify-email-sent", response_class=HTMLResponse)
async def verify_email_sent(request: Request):
    """Show email sent confirmation"""
    return templates.TemplateResponse(
        "auth/verify_email_sent.html",
        {"request": request}
    )

@router.get("/verify/{token}", response_class=HTMLResponse)
async def verify_email(request: Request, token: str, db: Session = Depends(get_db)):
    """Verify user email"""
    auth_service = AuthService(db)
    success = auth_service.verify_email(token)
    
    if success:
        return templates.TemplateResponse(
            "auth/verify_success.html",
            {"request": request}
        )
    else:
        return templates.TemplateResponse(
            "auth/verify_error.html",
            {"request": request}
        )

@router.post("/verify/resend")
async def resend_verification(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Resend verification email"""
    user = db.query(User).filter(User.email == email).first()
    
    if user and not user.email_verified:
        auth_service = AuthService(db)
        email_service = EmailService()
        
        token = auth_service.generate_email_verification_token(user.id)
        email_service.send_verification_email(email, user.full_name, token)
    
    return RedirectResponse(
        url="/auth/verify-email-sent",
        status_code=status.HTTP_302_FOUND
    )
