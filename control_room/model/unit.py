"""Data models for units"""

from enum import Enum
from datetime import datetime
from typing import Optional

class UnitStatus(Enum):
    """Unit status enumeration"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    UNAVAILABLE = "unavailable"

class Unit:
    """Unit model"""

    def __init__(
        self, 
        id: str,
        lat: float,
        lng: float,
        status: 'UnitStatus' = None,
        assigned_incident: Optional[str] = None
    ):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.status = status or UnitStatus.ACTIVE
        self.assigned_incident = assigned_incident

    def to_dict(self) -> dict:
        """Convert unit to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'lat': self.lat,
            'lng': self.lng,
            'status': self.status.value,
            'assigned_incident': self.assigned_incident
        }
