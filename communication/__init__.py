"""Communication module for abstracting communication between Control Room and ERT"""

from communication.channel import CommunicationChannel
from communication.message import Message, MessageType

__all__ = ['CommunicationChannel', 'Message', 'MessageType']
