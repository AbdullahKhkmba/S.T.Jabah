"""Data models for incidents"""

from enum import Enum
from datetime import datetime
from typing import Optional

class Unit:
    """Unit model"""

    def __init__(
        self, 
        id: str,
        x: float,
        y: float
    ):
        self.id = id
        self.x = x
        self.y = y


    def to_dict(self) -> dict:
        """Convert unit to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y
        }
