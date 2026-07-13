from sqlalchemy import Column, String, Float, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.base import BaseModel
import enum

class Platform(str, enum.Enum):
    GOOGLE_PLAY = "google_play"
    APP_STORE = "app_store"

class App(BaseModel):
    __tablename__ = "apps"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    platform = Column(Enum(Platform), nullable=False)
    package_name = Column(String(255), nullable=False, index=True)
    store_url = Column(String(500), nullable=False)
    app_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    country = Column(String(2), nullable=True)  # ISO country code
    aso_score = Column(Float, default=0.0)
    visibility_score = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="apps")
    audits = relationship("Audit", back_populates="app", cascade="all, delete-orphan")
    app_keywords = relationship("AppKeyword", back_populates="app", cascade="all, delete-orphan")
    competitors = relationship("Competitor", back_populates="app", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="app", cascade="all, delete-orphan")
    store_listing = relationship("StoreListing", back_populates="app", cascade="all, delete-orphan", uselist=False)
    creative_assets = relationship("CreativeAsset", back_populates="app", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="app")
    
    __table_args__ = (
        Index('idx_app_user_package', 'user_id', 'package_name', unique=True),
        Index('idx_app_aso_score', 'aso_score'),
        Index('idx_app_visibility', 'visibility_score'),
    )
