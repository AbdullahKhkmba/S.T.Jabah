"""Abstract communication channel for Control Room and ERT communication"""

from abc import ABC, abstractmethod
from communication.message import Message


class CommunicationChannel(ABC):
    """Abstract base class for communication channels"""
    
    @abstractmethod
    def send_message(self, recipient_id: str, message: Message):
        """
        Send a message to a recipient
        
        Args:
            recipient_id: ID of the recipient (unit_id or 'control_room')
            message: Message object to send
        """
        pass
    
    @abstractmethod
    def broadcast_message(self, recipient_ids: list, message: Message):
        """
        Broadcast a message to multiple recipients
        
        Args:
            recipient_ids: List of recipient IDs
            message: Message object to broadcast
        """
        pass
    
    @abstractmethod
    def receive_message(self, sender_id: str, message_type: str = None):
        """
        Receive messages from a sender
        
        Args:
            sender_id: ID of the sender
            message_type: Optional filter for message type
        
        Returns:
            List of Message objects
        """
        pass
    
    @abstractmethod
    def subscribe(self, recipient_id: str, callback):
        """
        Subscribe to messages for a recipient
        
        Args:
            recipient_id: ID of the recipient
            callback: Callback function to handle received messages
        """
        pass
