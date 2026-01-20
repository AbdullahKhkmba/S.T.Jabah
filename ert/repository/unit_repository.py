"""Data access layer for ERT unit persistence"""

from ert.model.unit import Unit
from abc import ABC, abstractmethod
from typing import TypeVar, Optional, List

T = TypeVar('T')

# This is an abstract repository interface for unit data operations.
class UnitRepository(ABC):
    """Abstract base repository interface defining common CRUD operations for Units"""
    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new unit in the database
        
        Args:
            entity: Unit object to create
        
        Returns:
            Created unit with ID
        """
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Retrieve unit by ID
        
        Args:
            entity_id: ID of the unit
        Returns:
            Unit object or None if not found
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Update unit in the database
        
        Args:
            entity: Unit object with updates
        
        Returns:
            Updated unit
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete unit by ID
        
        Args:
            entity_id: ID of the unit to delete
        
        Returns:
            True if deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def list_all(self) -> List[T]:
        """
        List all units in the database
        
        Returns:
            List of all unit objects
        """
        pass
    