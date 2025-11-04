"""
Audit event model for compliance and security logging
"""

from sqlalchemy import Column, String, DateTime, JSON, Index
from datetime import datetime

from .base import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True)
    actor_id = Column(String, nullable=False)  # User ID who performed action
    action = Column(String, nullable=False)  # view, export, submit, approve, etc.
    target_type = Column(String, nullable=False)  # flight, unit, report, etc.
    target_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Additional context
    event_metadata = Column(JSON)  # Additional event context
    ip_address = Column(String)
    user_agent = Column(String)

    # Indexes for audit queries
    __table_args__ = (
        Index('idx_audit_actor', 'actor_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_target', 'target_type', 'target_id'),
    )