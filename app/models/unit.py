"""
Unit model for military units
"""

from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(String, primary_key=True)  # e.g., "ea37b_55ecg"
    name = Column(String, nullable=False)  # e.g., "55th Electronic Combat Group"
    patch_image_url = Column(String)  # Unit patch/insignia image
    checklist_url = Column(String)  # URL to unit's ORM worksheet JSON
    last_updated = Column(DateTime, default=datetime.utcnow)

    # ORM Matrix configuration for this unit
    orm_matrix = Column(JSON)  # Stores ORMMatrix structure from worksheet

    # Relationships
    flights = relationship("Flight", back_populates="unit")

    # Indexes
    __table_args__ = (
        Index('idx_unit_name', 'name'),
    )