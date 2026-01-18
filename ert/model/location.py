"""Data models for location tracking"""

from datetime import datetime
from typing import Tuple, Optional


class Location:
    """Location model for GPS tracking"""
    
    def __init__(
        self,
        coordinates: Tuple[float, float],
        unit_id: str,
        timestamp: Optional[datetime] = None,
        metadata: Optional[dict] = None
    ):
        self.coordinates = coordinates  # (x, y) tuple
        self.unit_id = unit_id
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
