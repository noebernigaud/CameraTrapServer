from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# === Configuration ===
LOCAL_SAVE = False  # Set to False if you want to skip saving locally
UPLOAD_FOLDER = "videos"
NEXTCLOUD_URL = "https://bernigaudnoenextcloud.duckdns.org/remote.php/dav/files/agigas/ESP32-Videos/"
NEXTCLOUD_USERNAME = "agigas"
NEXTCLOUD_PASSWORD = "Leloupdu06!"  # or app password if 2FA is enabled

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Health Check ===
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "OK"}), 200

# === Upload Route ===
@app.route("/upload", methods=["POST"])
def upload():
    if "video" not in request.files:
        return jsonify({"error": "No video part in request"}), 400

    video = request.files["video"]
    if video.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.mp4"
    local_path = os.path.join(UPLOAD_FOLDER, filename)

    if LOCAL_SAVE:
        video.save(local_path)
        print(f"Saved video locally as {local_path}")
    else:
        video_stream = video.stream.read()
        with open(local_path, 'wb') as f:
            f.write(video_stream)

    # Upload to Nextcloud via WebDAV
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

# === Main ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
