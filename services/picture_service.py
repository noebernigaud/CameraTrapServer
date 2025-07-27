# picture_service.py
import os
from flask import jsonify
from constants.constants import UPLOAD_FOLDER

def save_picture(file, filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def save_picture_batch(files):
    saved_files = []
    for i, file in enumerate(files):
        filename = f"frame{i}.jpg"
        filepath = save_picture(file, filename)
        saved_files.append(filename)
    return jsonify({'status': 'ok', 'files': saved_files}), 200
