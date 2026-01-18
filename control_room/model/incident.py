"""Data models for incidents"""

from enum import Enum
from datetime import datetime
from typing import Optional


class IncidentStatus(Enum):
    """Incident status enumeration"""
    CREATED = "created"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class Incident:
    """Incident model"""

    def __init__(
        self,
        coordinates: tuple,
        id: Optional[str] = None,
        status: IncidentStatus = IncidentStatus.CREATED,
        assigned_unit_ids: Optional[list] = None,
        created_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
    ):
        self.id = id
        self.coordinates = coordinates  # (x, y) tuple
        self.status = status
        self.assigned_unit_ids = assigned_unit_ids or []
        self.created_at = created_at or datetime.now()
        self.resolved_at = resolved_at
    
    def to_dict(self) -> dict:
        """Convert incident to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'coordinates': list(self.coordinates) if self.coordinates else None,
            'status': self.status.value if isinstance(self.status, IncidentStatus) else str(self.status),
            'assigned_unit_ids': self.assigned_unit_ids,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
        }
