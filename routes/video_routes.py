# video_routes.py
from flask import Blueprint, request
from services.video_service import handle_upload

video_bp = Blueprint('video_bp', __name__)

@video_bp.route('/upload/video', methods=['POST'])
def upload_video():
    if "video" not in request.files:
        return {"error": "No video part in request"}, 400
    file = request.files["video"]
    if file.filename == "":
        return {"error": "No selected file"}, 400
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.mp4"
    return handle_upload(file, filename)
