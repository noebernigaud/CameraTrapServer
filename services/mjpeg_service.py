# mjpeg_service.py
import os
import cv2
import re
import requests
from datetime import datetime
from flask import jsonify
from constants.constants import UPLOAD_FOLDER, NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD

def process_mjpeg(request):
    content_type = request.headers.get('Content-Type', '')
    match = re.search(r'boundary=([^\s;]+)', content_type)
    if not match:
        return jsonify({'error': 'No boundary found'}), 400
    boundary = match.group(1)
    boundary_bytes = ('--' + boundary).encode()
    data = request.get_data()
    parts = data.split(boundary_bytes)
    saved_files = []
    for idx, part in enumerate(parts):
        if b'Content-Disposition' in part and b'filename=' in part:
            filename_match = re.search(b'filename="([^"]+)"', part)
            if filename_match:
                filename = filename_match.group(1).decode()
            else:
                filename = f'frame{idx}.jpg'
            header_end = part.find(b'\r\n\r\n')
            if header_end != -1:
                img_data = part[header_end+4:]
                img_data = img_data.rstrip(b'\r\n-')
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                saved_files.append(filepath)
    if not saved_files:
        return jsonify({'error': 'No files received'}), 400
    try:
        frames = [cv2.imread(f) for f in saved_files]
        frames = [f for f in frames if f is not None]
        if not frames:
            for f in saved_files:
                if os.path.exists(f):
                    os.remove(f)
            return jsonify({'error': 'No valid images'}), 400
        height, width, layers = frames[0].shape
        video_filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        video_path = os.path.join(UPLOAD_FOLDER, video_filename)
        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 5, (width, height))
        for frame in frames:
            out.write(frame)
        out.release()
        with open(video_path, "rb") as f:
            response = requests.put(
                NEXTCLOUD_URL + video_filename,
                data=f,
                auth=(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)
            )
        for f in saved_files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(video_path):
            os.remove(video_path)
        if response.status_code in [200, 201, 204]:
            return jsonify({"message": "Video uploaded to Nextcloud", "filename": video_filename}), 200
        else:
            return jsonify({"error": "Upload to Nextcloud failed", "status": response.status_code}), 500
    except Exception as e:
        for f in saved_files:
            if os.path.exists(f):
                os.remove(f)
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({"error": "Exception during video creation/upload", "details": str(e)}), 500
