"""
Configuration settings for ORM Dashboard API
Uses Pydantic settings for environment variable management
"""

from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./orm_dashboard.db"  # Default to SQLite for development

    # Security
    secret_key: str = "development-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS - Accept string or list to handle Railway environment variables
    allowed_origins: Union[str, List[str]] = ["http://localhost:3000", "http://localhost:3001"]

    @field_validator('allowed_origins')
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            # Handle comma-separated string from environment variable
            return [origin.strip() for origin in v.split(',')]
        return v

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
        # Railway might use different env var names
        database_env_vars = [
            "DATABASE_URL",
            "POSTGRES_URL",
            "POSTGRESQL_URL",
            "DATABASE_PRIVATE_URL",
            "DATABASE_PUBLIC_URL"
        ]

        for var in database_env_vars:
            if os.getenv(var):
                self.database_url = os.getenv(var)
                print(f"Using database from {var}: {self.database_url[:50]}...")
                break
        else:
            print(f"No database URL found. Checked: {database_env_vars}")
            print("Available env vars:", [k for k in os.environ.keys() if 'DATABASE' in k.upper() or 'POSTGRES' in k.upper()])

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