"""
User model for dashboard authentication and RBAC
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum, JSON, Index
from datetime import datetime

from .base import Base
from .enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # External user ID from SSO/CAC
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # Unit access control
    unit_access = Column(JSON)  # Array of unit IDs user can access

    # Permissions
    can_export = Column(Boolean, default=False)
    can_view_historical = Column(Boolean, default=True)
    can_view_pii = Column(Boolean, default=False)  # For current-day missions only

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # Indexes
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
        Index('idx_user_active', 'is_active'),
    )