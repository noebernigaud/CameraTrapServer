# mjpeg_routes.py
from flask import Blueprint, request
from services.mjpeg_service import process_mjpeg

mjpeg_bp = Blueprint('mjpeg_bp', __name__)

@mjpeg_bp.route('/upload/mjpeg', methods=['POST'])
def upload_mjpeg():
    return process_mjpeg(request)
