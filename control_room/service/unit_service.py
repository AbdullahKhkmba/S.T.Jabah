"""Business logic for Control Room incident management"""

import uuid
from control_room.model.incident import Incident, IncidentStatus
from control_room.repository.in_memory_unit_repository import InMemoryUnitRepository
from control_room.model.unit import Unit
from communication.websocket_communication import WebSocketCommunication
from typing import List

class UnitService:
    """Service layer for unit operations"""
    
    def __init__(self, unit_repository: InMemoryUnitRepository, communication_channel: WebSocketCommunication):
        self.unit_repository = unit_repository
        self.communication_channel = communication_channel
    
    def create_unit(self,id, x, y: float) -> Unit:
        """
        Create a new unit in the system
        
        Args:
            x: X coordinate
            y: Y coordinate
        
        Returns:
            Created unit object
        """
        unit = Unit(
            id=id,
            x=x,
            y=y,
        )
        created_unit = self.unit_repository.create(unit)

        # Notify ERT units about the new unit
        # self.communication_channel.notify_units_new_unit(created_unit)
        
        return created_unit
    
    def get_unit_by_id(self, unit_id: str):
        """
        Retrieve unit by ID from repository
        
        Args:
            unit_id: ID of the unit to retrieve
        
        Returns:
            Unit object if found, None otherwise
        """
        return self.unit_repository.get_by_id(unit_id)
    
    def update_unit(self, unit_id: str, x: float, y: float):
        """
        Update unit coordinates

        Args:
            unit_id: ID of the unit
            x: New x coordinate
            y: New y coordinate
        """
        unit = self.unit_repository.get_by_id(unit_id)
        if not unit:
            raise ValueError(f"Unit with ID {unit_id} does not exist.")
        
        unit.x = x
        unit.y = y
        updated_unit = self.unit_repository.update(unit)
        return updated_unit
        
    def get_all_units(self) -> List[Unit]:
        """
        Get all units in the system
        """
        return self.unit_repository.get_all()
    
    def delete_unit(self, unit_id: str) -> bool:
        """
        Delete a unit from the system
        
        Args:
            unit_id: The unique identifier of the unit to delete
            
        Returns:
            True if unit was deleted successfully, False if unit was not found
        """
        return self.unit_repository.delete(unit_id)
    