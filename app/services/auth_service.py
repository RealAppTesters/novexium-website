from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID
import bcrypt
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.user import User, SubscriptionPlan, SubscriptionStatus
from app.models.session import Session as UserSession
from app.models.audit_log import AuditLog

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_user(self, email: str, full_name: str, password: str) -> User:
        """Create a new user"""
        # Check if user exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create user
        user = User(
            email=email,
            full_name=full_name,
            password_hash=self.hash_password(password),
            subscription_plan=SubscriptionPlan.FREE,
            subscription_status=SubscriptionStatus.TRIAL,
            trial_start=datetime.utcnow(),
            trial_end=datetime.utcnow() + timedelta(days=7)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Log activity
        self._log_activity(user.id, "user_registered", {"email": email})
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        # Log activity
        self._log_activity(user.id, "user_login", {"email": email})
        
        return user
    
    def create_session(self, user_id: UUID, ip_address: str = None, 
                       user_agent: str = None, remember_me: bool = False) -> UserSession:
        """Create a new user session"""
        # Delete old sessions for this user (keep last 5)
        sessions = self.db.query(UserSession).filter(
            UserSession.user_id == user_id
        ).order_by(UserSession.created_at.desc()).offset(5).all()
        
        for session in sessions:
            self.db.delete(session)
        
        # Create new session
        expires_at = datetime.utcnow() + timedelta(days=30 if remember_me else 7)
        
        session = UserSession(
            user_id=user_id,
            token=self._generate_session_token(),
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def get_session(self, token: str) -> Optional[UserSession]:
        """Get a session by token"""
        session = self.db.query(UserSession).filter(
            UserSession.token == token,
            UserSession.expires_at > datetime.utcnow()
        ).first()
        
        if session:
            # Update last used (optional)
            pass
        
        return session
    
    def delete_session(self, token: str) -> bool:
        """Delete a session"""
        session = self.db.query(UserSession).filter(
            UserSession.token == token
        ).first()
        
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        
        return False
    
    def delete_all_sessions(self, user_id: UUID, current_token: str = None) -> int:
        """Delete all sessions for a user except current one"""
        query = self.db.query(UserSession).filter(
            UserSession.user_id == user_id
        )
        
        if current_token:
            query = query.filter(UserSession.token != current_token)
        
        count = query.count()
        query.delete()
        self.db.commit()
        
        return count
    
    def generate_password_reset_token(self, email: str) -> str:
        """Generate a password reset token"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create JWT token
        token = jwt.encode(
            {
                "user_id": str(user.id),
                "type": "password_reset",
                "exp": datetime.utcnow() + timedelta(hours=24)
            },
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        
        return token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset a user's password using a token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            if payload.get("type") != "password_reset":
                return False
            
            user_id = UUID(payload.get("user_id"))
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            user.password_hash = self.hash_password(new_password)
            self.db.commit()
            
            # Log activity
            self._log_activity(user.id, "password_reset", {})
            
            return True
            
        except jwt.PyJWTError:
            return False
    
    def generate_email_verification_token(self, user_id: UUID) -> str:
        """Generate an email verification token"""
        token = jwt.encode(
            {
                "user_id": str(user_id),
                "type": "email_verification",
                "exp": datetime.utcnow() + timedelta(days=7)
            },
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        
        return token
    
    def verify_email(self, token: str) -> bool:
        """Verify a user's email using a token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            if payload.get("type") != "email_verification":
                return False
            
            user_id = UUID(payload.get("user_id"))
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False
            
            user.email_verified = True
            self.db.commit()
            
            # Log activity
            self._log_activity(user.id, "email_verified", {})
            
            return True
            
        except jwt.PyJWTError:
            return False
    
    def _log_activity(self, user_id: UUID, action: str, details: Dict[str, Any]):
        """Log user activity"""
        log = AuditLog(
            user_id=user_id,
            action=action,
            details=details
        )
        self.db.add(log)
        self.db.commit()
    
    def _generate_session_token(self) -> str:
        """Generate a random session token"""
        import secrets
        return secrets.token_urlsafe(64)
