"""Data access layer for ERT unit persistence"""

from ert.model.unit import Unit


class UnitRepository:
    """Repository for unit data operations"""
    
    def get_by_id(self, unit_id: str) -> Unit:
        """
        Retrieve unit by ID
        
        Args:
            unit_id: ID of the unit
        
        Returns:
            Unit object or None if not found
        """
        pass
    
    def update(self, unit: Unit) -> Unit:
        """
        Update unit in the database
        
        Args:
            unit: Unit object with updates
        
        Returns:
            Updated unit
        """
        pass
    
    def update_location(self, unit_id: str, coordinates: tuple):
        """
        Update unit's current location
        
        Args:
            unit_id: ID of the unit
            coordinates: Tuple of (x, y) coordinates
        """
        pass
    
    def get_assigned_incidents(self, unit_id: str) -> list:
        """
        Get all incidents assigned to a unit
        
        Args:
            unit_id: ID of the unit
        
        Returns:
            List of incident IDs
        """
        pass
