"""
Configuration settings for ORM Dashboard API
Uses Pydantic settings for environment variable management
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./orm_dashboard.db"  # Default to SQLite for development

    # Security
    secret_key: str = "development-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Application
    environment: str = "development"
    sql_debug: bool = False

    # Server
    port: int = 8000
    host: str = "0.0.0.0"

    class Config:
        # Don't try to load .env file in production to avoid JSON parsing issues
        env_file = ".env" if os.getenv("RAILWAY_ENVIRONMENT") is None else None
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Handle production environment variables
        if os.getenv("DATABASE_URL"):
            self.database_url = os.getenv("DATABASE_URL")

        if os.getenv("SECRET_KEY"):
            self.secret_key = os.getenv("SECRET_KEY")

        if os.getenv("PORT"):
            self.port = int(os.getenv("PORT"))

        if os.getenv("ALLOWED_ORIGINS"):
            self.allowed_origins = os.getenv("ALLOWED_ORIGINS").split(",")

# Global settings instance with error handling
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    # Fallback to basic settings
    import sys
    settings = Settings(_env_file=None)
    print("Loaded fallback settings")