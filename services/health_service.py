# health_service.py
from flask import jsonify

def ping():
    return jsonify({"status": "OK"}), 200
