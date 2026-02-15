"""WebSocket message handlers for Control Room subscriptions

Handlers moved out of the service layer to a dedicated module so
the communication layer can subscribe to them directly.
"""
from control_room.model.incident import IncidentStatus
from typing import Any

class WebSocketHandlers:
    def __init__(self, incident_repository, unit_service=None):
        self.incident_repository = incident_repository
        self.unit_service = unit_service

    async def handle_location(self, data: dict):
        print(f"[Control Room] 📍 Vehicle Location: {data}")

    async def handle_acknowledgment(self, data: dict):
        print(f"[Control Room] ✅ Acknowledgment: {data}")

        ert_id = data.get("ert_id")
        incident_id = data.get("incident_id")

        # Create new ert unit if not already exists (unit_service is optional)
        if self.unit_service:
            try:
                unit = self.unit_service.get_unit_by_id(ert_id)
                if not unit:
                    self.unit_service.create_unit(ert_id, data.get("x"), data.get("y"))
            except Exception as e:
                print(f"[Control Room] ❌ Failed to create ERT Unit: {ert_id} ({e})")

        # Add the ert unit to the incident's assigned units list
        incident = self.incident_repository.get_by_id(incident_id)
        if incident and ert_id not in incident.assigned_units:
            incident.assigned_units.append(ert_id)
            self.incident_repository.update(incident)

        # Update incident status to acknowledged if it was created before
        if incident and incident.status == IncidentStatus.DISPATCHED:
            incident.status = IncidentStatus.ACKNOWLEDGED
            self.incident_repository.update(incident)

    async def handle_resolution(self, data: dict):
        print(f"[Control Room] 🎉 Resolution: {data}")
