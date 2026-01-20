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
    
    def __init__(self, id: str):
        self.id = id
    
    def to_dict(self) -> dict:
        """Convert unit to dictionary for JSON serialization"""
        return {
            'id': self.id
        }
