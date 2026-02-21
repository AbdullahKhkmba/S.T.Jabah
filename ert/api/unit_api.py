"""API handlers for ERT unit endpoints"""

from flask import Blueprint, json, request, jsonify
import logging
import asyncio

from ert.service.unit_service import UnitService

logger = logging.getLogger(__name__)

ert_bp = Blueprint('ert', __name__)

def init_ert_api(unit_service: UnitService):
    """Initialize the ERT API with service dependencies"""
    ert_bp.unit_service = unit_service
    return ert_bp

@ert_bp.route('/unit/location', methods=['GET'])
def get_unit_location():
    try:
        with open("ert/unit_info.json", "r") as f:
            unit_info = json.load(f)
            location = {
                "x": unit_info["x"],
                "y": unit_info["y"]
            }
        return jsonify(location), 200
    except Exception as e:
        logger.error(f"Error retrieving unit location: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@ert_bp.route('/incident/location', methods=['GET'])
def get_incident_location():
    try:
        with open("ert/unit_info.json", "r") as f:
            unit_info = json.load(f)
            location = {
                "x": unit_info["assigned_incident"]["x"],
                "y": unit_info["assigned_incident"]["y"]
            }
        return jsonify(location), 200
    except Exception as e:
        logger.error(f"Error retrieving incident location: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500
    
@ert_bp.route('/incident/resolve', methods=['PUT'])
def resolve_incident():
    try:
        # check that an incident is assigned to the unit before trying to resolve it
        with open("ert/unit_info.json", "r") as f:
            unit_info = json.load(f)
            if unit_info["assigned_incident"] is None:
                return jsonify({
                    'error': 'No incident assigned to this unit'
                }), 400
            
        asyncio.run(ert_bp.unit_service.resolve_incident())

        return jsonify({
            'message': 'Incident resolved successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error resolving incident: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500