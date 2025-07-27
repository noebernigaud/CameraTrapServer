# picture_routes.py
from flask import Blueprint, request
from services.picture_service import save_picture_batch
from services.video_service import handle_upload

picture_bp = Blueprint('picture_bp', __name__)

@picture_bp.route('/upload/picture', methods=['POST'])
def upload_picture():
    if "picture" not in request.files:
        return {"error": "No picture part in request"}, 400
    file = request.files["picture"]
    if file.filename == "":
        return {"error": "No selected file"}, 400
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"picture_{timestamp}.jpg"
    return handle_upload(file, filename)

@picture_bp.route('/upload/multipart', methods=['POST'])
def upload_picture_batch():
    files = request.files.getlist('picture')
    if not files:
        return {"error": "No files received"}, 400
    return save_picture_batch(files)
