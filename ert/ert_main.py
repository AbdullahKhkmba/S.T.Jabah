import asyncio
import sys
from pathlib import Path

# Add parent directory to Python path to resolve imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from communication.websocket_communication import WebSocketCommunication

# ERT Configuration
ERT_ID = "ERT-001"  # Unique identifier for this ERT unit

# --- Callbacks ---
async def on_new_incident(data):
    """Handle incoming incident from control room"""
    print(f"\n[ERT-{ERT_ID}] 🚨 RECEIVED INCIDENT: {data}")
    print(f"[ERT-{ERT_ID}] Preparing vehicle...")
    
    # Extract incident ID
    incident_id = data.get('id', 'unknown')
    
    # Send acknowledgment to control room
    # Acknowledgment contains: ERT id, incident id, and success message
    acknowledgment = {
        "ert_id": ERT_ID,
        "incident_id": incident_id,
        "message": "Incident received successfully. ERT unit dispatched.",
        "status": "acknowledged"
    }
    
    await ert_comms.publish("acknowledgment", acknowledgment)
    print(f"[ERT-{ERT_ID}] ✅ Acknowledgment sent to control room")

# --- Main ERT Logic ---
ert_comms = WebSocketCommunication()

async def main():
    # 1. Connect to Hub (Replace localhost with Control Room Domain/IP)
    await ert_comms.connect("ws://localhost:8765")
    print(f"[ERT-{ERT_ID}] Connected to control room hub")
    
    # 2. Subscribe to Incidents
    await ert_comms.subscribe("new_incident", on_new_incident)
    print(f"[ERT-{ERT_ID}] Subscribed to incident notifications")
    
    # 3. Simulation Loop (sending location updates)
    while True:
        # Simulate GPS coordinates
        location_data = {
            "ert_id": ERT_ID,
            "lat": 30.0444, 
            "lng": 31.2357, 
            "speed": 60
        }
        
        print(f"[ERT-{ERT_ID}] Sending Location...")
        await ert_comms.publish("location", location_data)
        
        await asyncio.sleep(5) # Send every 5 seconds

if __name__ == "__main__":
    asyncio.run(main())