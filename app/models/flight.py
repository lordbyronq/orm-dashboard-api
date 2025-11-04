"""
Flight and related models for ORM data
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey, Enum, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import Base
from .enums import SeverityLevel

class Flight(Base):
    __tablename__ = "flights"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    unit_id = Column(String, ForeignKey("units.id"), nullable=False)

    # Flight information (PII fields - will be sanitized for historical data)
    flight_date = Column(DateTime, nullable=False)
    aircraft_commander = Column(String)  # PII - sanitized after 24 hours
    callsign = Column(String)  # PII - sanitized after 24 hours
    tail_number = Column(String)  # Potentially sensitive
    aircraft_type = Column(String)  # Derived from tail number
    mission_type = Column(String)

    # ORM risk data
    total_risk_score = Column(Integer, default=0)
    risk_tier = Column(Enum(SeverityLevel), default=SeverityLevel.LOW)
    crew_count = Column(Integer, default=0)
    average_crew_risk = Column(Enum(SeverityLevel), default=SeverityLevel.LOW)

    # Status tracking
    is_briefed = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    approval_by = Column(String)  # Role for historical, name for current
    required_approval = Column(String)

    # Metadata
    last_edited = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    template_version = Column(String)
    schema_version = Column(Integer, default=1)
    is_pii_scrubbed = Column(Boolean, default=False)

    # Snapshot of ORM matrix used for this flight
    orm_matrix_snapshot = Column(JSON)

    # Relationships
    unit = relationship("Unit", back_populates="flights")
    hazard_responses = relationship("FlightHazard", back_populates="flight", cascade="all, delete-orphan")
    crew_members = relationship("CrewMember", back_populates="flight", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        Index('idx_flight_unit_date', 'unit_id', 'flight_date'),
        Index('idx_flight_risk_tier', 'risk_tier'),
        Index('idx_flight_status', 'is_approved', 'is_briefed'),
    )

class FlightHazard(Base):
    __tablename__ = "flight_hazards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    flight_id = Column(String, ForeignKey("flights.id"), nullable=False)

    # Hazard information snapshot
    hazard_id = Column(String, nullable=False)  # Original hazard ID from worksheet
    hazard_name = Column(String, nullable=False)
    hazard_snapshot = Column(JSON)  # Full hazard structure at time of response

    # Response data
    selected_option_id = Column(String)
    selected_option_label = Column(String)
    selected_severity = Column(Enum(SeverityLevel))
    score = Column(Integer, default=0)

    # Relationships
    flight = relationship("Flight", back_populates="hazard_responses")

    # Indexes
    __table_args__ = (
        Index('idx_hazard_flight_id', 'flight_id'),
        Index('idx_hazard_name', 'hazard_name'),
        Index('idx_hazard_severity', 'selected_severity'),
    )

class CrewMember(Base):
    __tablename__ = "crew_members"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    flight_id = Column(String, ForeignKey("flights.id"), nullable=False)

    # Crew information (PII - will be sanitized)
    name = Column(String)  # PII - sanitized after 24 hours
    position = Column(String)  # e.g., "Pilot", "Navigator", "EWO"

    # ORM assessment
    total_score = Column(Integer, default=0)
    risk_level = Column(Enum(SeverityLevel), default=SeverityLevel.LOW)
    responses = Column(JSON)  # Array of crew ORM responses

    # Metadata
    showtime = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    flight = relationship("Flight", back_populates="crew_members")

    # Indexes
    __table_args__ = (
        Index('idx_crew_flight_id', 'flight_id'),
        Index('idx_crew_risk_level', 'risk_level'),
    )