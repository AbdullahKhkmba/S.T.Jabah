"""Message models for communication"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class MessageType(Enum):
    """Message type enumeration"""
    INCIDENT_DISPATCH = "incident_dispatch"
    ACKNOWLEDGMENT = "acknowledgment"
    LOCATION_UPDATE = "location_update"
    RESOLUTION = "resolution"
    STATUS_UPDATE = "status_update"


class Message:
    """Message model for communication between Control Room and ERT"""
    
    def __init__(
        self,
        message_type: MessageType,
        sender_id: str,
        recipient_id: str,
        payload: Dict[str, Any],
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        self.message_id = message_id
        self.message_type = message_type
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.payload = payload
        self.timestamp = timestamp or datetime.now()
