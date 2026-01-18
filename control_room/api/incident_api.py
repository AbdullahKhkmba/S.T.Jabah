"""API handlers for Control Room incident endpoints"""

from flask import Blueprint, request, jsonify
import logging

from control_room.service.incident_service import IncidentService

logger = logging.getLogger(__name__)

control_room_bp = Blueprint('control_room', __name__)

def init_control_room_api(incident_service: IncidentService):
    """Initialize the Control Room API with service dependencies"""
    control_room_bp.incident_service = incident_service
    return control_room_bp

@control_room_bp.route('/incidents', methods=['POST'])
def create_incident():
    """Create a new incident"""
    logger.info("API: Creating new incident")
    data = request.json
    
    if not data or 'coordinates' not in data:
        return jsonify({'error': 'Missing required fields: coordinates (x, y)'}), 400
    
    service: IncidentService = control_room_bp.incident_service
    coordinates = data.get('coordinates')
    
    # Ensure coordinates is a tuple (x, y)
    if isinstance(coordinates, list) and len(coordinates) == 2:
        coordinates = tuple(coordinates)
    elif not isinstance(coordinates, (tuple, list)):
        return jsonify({'error': 'Invalid coordinates format. Expected [x, y] or {"x": x, "y": y}'}), 400
    
    incident = service.create_incident(coordinates)
    
    if incident:
        return jsonify(incident.to_dict()), 201
    return jsonify({'error': 'Failed to create incident'}), 500

@control_room_bp.route('/incidents', methods=['GET'])
def get_all_incidents():
    """Get all incidents"""
    logger.info("API: Getting all incidents")
    service: IncidentService = control_room_bp.incident_service
    
    incidents = service.incident_repository.get_all()
    return jsonify([incident.to_dict() for incident in incidents]), 200


@control_room_bp.route('/incidents/<incident_id>', methods=['GET'])
def get_incident_by_id(incident_id):
    """Get a specific incident by ID"""
    logger.info(f"API: Getting incident {incident_id}")
    service: IncidentService = control_room_bp.incident_service
    
    incident = service.incident_repository.get_by_id(incident_id)
    
    if incident:
        return jsonify(incident.to_dict()), 200
    return jsonify({'error': 'Incident not found'}), 404


@control_room_bp.route('/incidents/<incident_id>', methods=['PUT'])
def update_incident(incident_id):
    """Update an existing incident"""
    logger.info(f"API: Updating incident {incident_id}")
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    service: IncidentService = control_room_bp.incident_service
    
    # Get existing incident
    incident = service.incident_repository.get_by_id(incident_id)
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    
    # Update fields
    if 'coordinates' in data:
        coords = data['coordinates']
        if isinstance(coords, list) and len(coords) == 2:
            incident.coordinates = tuple(coords)
        else:
            return jsonify({'error': 'Invalid coordinates format'}), 400
    
    if 'status' in data:
        from control_room.model.incident import IncidentStatus
        try:
            incident.status = IncidentStatus(data['status'])
        except ValueError:
            return jsonify({'error': 'Invalid status value'}), 400
    
    if 'assigned_unit_ids' in data:
        incident.assigned_unit_ids = data['assigned_unit_ids']
    
    # Save updated incident
    updated_incident = service.incident_repository.update(incident)
    
    if updated_incident:
        return jsonify(updated_incident.to_dict()), 200
    return jsonify({'error': 'Failed to update incident'}), 500


@control_room_bp.route('/incidents/<incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """Delete an incident"""
    logger.info(f"API: Deleting incident {incident_id}")
    service: IncidentService = control_room_bp.incident_service
    
    success = service.incident_repository.delete(incident_id)
    
    if success:
        return jsonify({'message': 'Incident deleted successfully'}), 200
    return jsonify({'error': 'Incident not found'}), 404


@control_room_bp.route('/incidents/<incident_id>/dispatch', methods=['POST'])
def dispatch_incident(incident_id):
    """Dispatch incident to specific ERT vehicles"""
    logger.info(f"API: Dispatching incident {incident_id}")
    data = request.json
    
    unit_ids = data.get('unit_ids', []) if data else []
    if not unit_ids:
        return jsonify({'error': 'No units selected'}), 400
    
    service: IncidentService = control_room_bp.incident_service
    result = service.dispatch_incident(incident_id, unit_ids)
    
    if result:
        return jsonify({'status': 'Units dispatched'}), 200
    return jsonify({'error': 'Failed to dispatch incident'}), 500
