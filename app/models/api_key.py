from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel

class APIKey(BaseModel):
    __tablename__ = "api_keys"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    api_key = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    permissions = Column(JSON, nullable=True)  # Store as JSON array of permissions
    last_used = Column(DateTime(timezone=True), nullable=True)
    expiry = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    __table_args__ = (
        Index('idx_apikey_user_expiry', 'user_id', 'expiry'),
        Index('idx_apikey_last_used', 'last_used'),
    )
