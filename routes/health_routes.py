# health_routes.py
from flask import Blueprint
from services.health_service import ping

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/ping', methods=['GET'])
def health_check():
    return ping()
