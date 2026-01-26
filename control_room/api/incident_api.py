"""API handlers for Control Room incident endpoints"""
from control_room.model.incident import Incident
from flask import Blueprint, request, jsonify
import logging
from control_room.repository.in_memory_incident_repository import InMemoryIncidentRepository
from control_room.service.incident_service import IncidentService

logger = logging.getLogger(__name__)

control_room_bp = Blueprint('control_room', __name__)

def init_control_room_api(incident_service: IncidentService):
    """Initialize the Control Room API with service dependencies"""
    control_room_bp.incident_service = incident_service
    return control_room_bp

@control_room_bp.route('/incidents/<incident_id>', methods=['GET'])
def get_incident(incident_id: str):
    try:
        incident = control_room_bp.incident_service.get_incident_by_id(incident_id)

        if incident is None:
            return jsonify({
                'error': 'Incident not found',
                'incident_id': incident_id
            }), 404
        
        return jsonify(incident.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error retrieving incident {incident_id}: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@control_room_bp.route('/incidents', methods=['GET'])
def list_incidents():
    try:
        incidents = control_room_bp.incident_service.get_all_incidents()
        incidents_data = [incident.to_dict() for incident in incidents]
        
        return jsonify(incidents_data), 200
        
    except Exception as e:
        logger.error(f"Error listing incidents: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500