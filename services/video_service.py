# video_service.py
import os
import requests
from datetime import datetime
from flask import jsonify
from constants.constants import UPLOAD_FOLDER, NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, LOCAL_SAVE

def handle_upload(file, filename):
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    if LOCAL_SAVE:
        file.save(local_path)
        print(f"Saved file locally as {local_path}")
    else:
        file_stream = file.stream.read()
        with open(local_path, 'wb') as f:
            f.write(file_stream)
    try:
        with open(local_path, "rb") as f:
            response = requests.put(
                NEXTCLOUD_URL + filename,
                data=f,
                auth=(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)
            )
        if response.status_code in [200, 201, 204]:
            print(f"Uploaded {filename} to Nextcloud successfully.")
            return jsonify({"message": "Uploaded to Nextcloud", "filename": filename}), 200
        else:
            print(f"Failed to upload to Nextcloud: {response.status_code} {response.text}")
            return jsonify({"error": "Upload to Nextcloud failed", "status": response.status_code}), 500
    except Exception as e:
        print(f"Error during Nextcloud upload: {e}")
        return jsonify({"error": "Exception during upload", "details": str(e)}), 500
