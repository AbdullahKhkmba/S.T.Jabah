"""API handlers for ERT unit endpoints"""

from flask import Blueprint, request, jsonify
import logging

from ert.service.unit_service import UnitService

logger = logging.getLogger(__name__)

ert_bp = Blueprint('ert', __name__)


def init_ert_api(unit_service: UnitService):
    """Initialize the ERT API with service dependencies"""
    ert_bp.unit_service = unit_service
    return ert_bp


@ert_bp.route('/units/<unit_id>/active', methods=['GET'])
def get_active(unit_id):
    """Get active assignment for a unit"""
    logger.info(f"API: Getting active assignment for unit {unit_id}")
    service: UnitService = ert_bp.unit_service
    
    incident = service.get_active_assignment(unit_id)
    
    if not incident:
        return jsonify({'message': 'No active assignments'}), 204
    return jsonify(incident.to_dict() if hasattr(incident, 'to_dict') else incident), 200


@ert_bp.route('/units/<unit_id>/acknowledge', methods=['PATCH'])
def acknowledge(unit_id):
    """Unit acknowledges the task and signals it is moving"""
    logger.info(f"API: Unit {unit_id} acknowledging task")
    data = request.json or {}
    
    incident_id = data.get('incident_id')
    if not incident_id:
        return jsonify({'error': 'Missing incident_id'}), 400
    
    service: UnitService = ert_bp.unit_service
    result = service.acknowledge_incident(unit_id, incident_id)
    
    if result:
        return jsonify({'status': 'Acknowledged'}), 200
    return jsonify({'error': 'Failed to acknowledge'}), 500


@ert_bp.route('/units/<unit_id>/location', methods=['POST'])
def post_location(unit_id):
    """ERT vehicle streams GPS coordinates to Control Room"""
    logger.info(f"API: Unit {unit_id} updating location")
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Support both {"x": x, "y": y} and {"coordinates": [x, y]} formats
    if 'x' in data and 'y' in data:
        coordinates = (data['x'], data['y'])
    elif 'coordinates' in data:
        coords = data['coordinates']
        if isinstance(coords, list) and len(coords) == 2:
            coordinates = tuple(coords)
        else:
            return jsonify({'error': 'Invalid coordinates format'}), 400
    else:
        return jsonify({'error': 'Missing coordinates (x, y) or coordinates array'}), 400
    
    service: UnitService = ert_bp.unit_service
    result = service.update_unit_location(unit_id, coordinates)
    
    if result:
        return jsonify({'status': 'Location updated'}), 200
    return jsonify({'error': 'Failed to update location'}), 500


@ert_bp.route('/units/<unit_id>/resolve', methods=['PATCH'])
def resolve_task(unit_id):
    """Unit resolves task, system checks if incident can close"""
    logger.info(f"API: Unit {unit_id} resolving task")
    data = request.json or {}
    
    incident_id = data.get('incident_id')
    if not incident_id:
        return jsonify({'error': 'Missing incident_id'}), 400
    
    service: UnitService = ert_bp.unit_service
    result = service.resolve_incident(unit_id, incident_id)
    
    if result:
        return jsonify(result if isinstance(result, dict) else {'status': 'Resolved'}), 200
    return jsonify({'error': 'Failed to resolve task'}), 500
