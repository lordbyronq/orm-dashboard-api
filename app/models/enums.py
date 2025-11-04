"""
Enums used across the application
"""

import enum

class SeverityLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

class UserRole(enum.Enum):
    UNIT_LEAD = "UNIT_LEAD"
    SAFETY_OFFICER = "SAFETY_OFFICER"
    GROUP_LEAD = "GROUP_LEAD"
    WING_LEAD = "WING_LEAD"
    ADMIN = "ADMIN"