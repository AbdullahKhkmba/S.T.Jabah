"""Business logic for ERT unit operations"""

import json
from random import random


class UnitService:
    """Service layer for ERT unit operations"""
    
    def __init__(self, communication_channel=None):
        self.communication_channel = communication_channel
    
    def update_gps_location(self):
        """
        Update unit location and stream to Control Room
        
        Args:
            unit_id: ID of the ERT unit
            coordinates: Tuple of (x, y) GPS coordinates
        """
        # generate random coordinates for simulation
        x = random() * 100
        y = random() * 100
        print(f"Updated GPS location: ({x:.2f}, {y:.2f})")
        with open("ert/unit_info.json", "r") as f:
            unit_info = json.load(f)
            unit_info["x"] = x
            unit_info["y"] = y
        with open("ert/unit_info.json", "w") as f:
            json.dump(unit_info, f, indent=4)
    
    async def resolve_incident(self):
        """
        1- Update unit status to resolved in the ERT repository (unit_info.json)
        2- Notify Control Room about the resolution so it can update the incident status in its

        Args:
            unit_id: ID of the ERT unit
            incident_id: ID of the incident
        """
        with open("ert/unit_info.json", "r") as f:
            unit_info = json.load(f)
        
        # Capture incident ID before clearing it
        incident_id = unit_info["assigned_incident"]["id"] if unit_info["assigned_incident"] else None
        
        # Update status and clear assigned incident
        unit_info["status"] = "resolved"
        unit_info["assigned_incident"] = None
        with open("ert/unit_info.json", "w") as f:
            json.dump(unit_info, f, indent=4)
        
        # Notify Control Room about the resolution
        if self.communication_channel:
            resolution_data = {
                "ert_id": unit_info["id"],
            }
            print(f"[ERT-{unit_info['id']}] 🎉 Incident resolved, notifying Control Room...")
            await self.communication_channel.publish("resolution", resolution_data)