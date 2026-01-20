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

