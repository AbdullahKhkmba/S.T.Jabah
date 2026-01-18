"""Service for computing paths from unit location to incident"""


class PathService:
    """Service for path computation"""
    
    def compute_path(self, from_coordinates: tuple, to_coordinates: tuple):
        """
        Compute path from current location to incident coordinates
        
        Args:
            from_coordinates: Tuple of (x, y) - current unit location
            to_coordinates: Tuple of (x, y) - incident location
        
        Returns:
            Path data structure (list of waypoints, route, etc.)
        """
        pass
