from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Novexium"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
