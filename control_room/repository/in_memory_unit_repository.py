"""In-memory implementation of Incident repository (for testing/development)"""
import uuid
import datetime
from abc import abstractmethod
from typing import Optional, List
from control_room.model.incident import Incident
from control_room.model.unit import Unit
from control_room.repository.unit_repository import UnitRepository

class InMemoryUnitRepository(UnitRepository):
    """In-memory implementation of Unit repository using dictionary storage"""

    def __init__(self):
        self._storage: dict[str, Unit] = {}

    def create(self, entity: Unit) -> Unit:
        """
        Create a new entity in the database
        
        Args:
            entity: Entity object to create
        
        Returns:
            Created entity with ID
        """
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[Unit]:
        """
        Retrieve entity by ID from storage
        
        Args:
            entity_id: ID of the entity to retrieve
        
        Returns:
            Entity object if found, None otherwise
        """
        return self._storage.get(entity_id)

    def update(self, entity: Incident) -> Incident:
        """
        Update entity in the database
        
        Args:
            entity: Entity object with updates
        
        Returns:
            Updated entity
        """
        if entity.id in self._storage:
            self._storage[entity.id] = entity
            return entity
        raise ValueError(f"Entity with ID {entity.id} does not exist.")
    
    def delete(self, entity_id: str) -> bool:
        """
        Delete entity by ID
        
        Args:
            entity_id: ID of the entity to delete
        
        Returns:
            True if deleted, False otherwise
        """
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def get_all(self) -> Incident:
        """
        Get all entities
        
        Returns:
            List of all entities
        """
        return list(self._storage.values())