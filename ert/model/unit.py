"""Data models for ERT units"""

from enum import Enum
from typing import Optional, Tuple
from datetime import datetime


class UnitStatus(Enum):
    """Unit status enumeration"""
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    ON_SCENE = "on_scene"
    RESOLVED = "resolved"


class Unit:
    """ERT unit model"""
    
    def __init__(
        self,
        id: str,
        current_location: Optional[Tuple[float, float]] = None,
        status: UnitStatus = UnitStatus.AVAILABLE,
        assigned_incident_ids: Optional[list] = None,
        last_updated: Optional[datetime] = None,
        metadata: Optional[dict] = None
    ):
        self.id = id
        self.current_location = current_location  # (x, y) tuple
        self.status = status
        self.assigned_incident_ids = assigned_incident_ids or []
        self.last_updated = last_updated or datetime.now()
        self.metadata = metadata or {}
    
    def to_dict(self) -> dict:
        """Convert unit to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'current_location': list(self.current_location) if self.current_location else None,
            'status': self.status.value if isinstance(self.status, UnitStatus) else str(self.status),
            'assigned_incident_ids': self.assigned_incident_ids,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'metadata': self.metadata
        }
