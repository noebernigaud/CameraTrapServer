from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# === Configuration ===
LOCAL_SAVE = False  # Set to False if you want to skip saving locally
UPLOAD_FOLDER = "uploads"  # Changed to more generic name
NEXTCLOUD_URL = "https://bernigaudnoenextcloud.duckdns.org/remote.php/dav/files/agigas/ESP32-Videos/"
NEXTCLOUD_USERNAME = "agigas"
NEXTCLOUD_PASSWORD = "Leloupdu06!"  # or app password if 2FA is enabled

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Health Check ===
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "OK"}), 200

# === Video Upload Route ===
@app.route("/upload/video", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video part in request"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.mp4"
    return handle_upload(file, filename)
    
@app.route('/upload/mjpeg', methods=['POST'])
def upload_picture_stream():
    files = request.files.getlist('picture')
    if not files:
        return jsonify({'error': 'No files received'}), 400

    saved_files = []
    for i, file in enumerate(files):
        # Use timestamp and index for unique filenames
        filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{i}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        saved_files.append(filename)

    return jsonify({'status': 'ok', 'files': saved_files}), 200

# === Picture Upload Route ===
@app.route("/upload/picture", methods=["POST"])
def upload_picture():
    if "picture" not in request.files:
        return jsonify({"error": "No picture part in request"}), 400

    file = request.files["picture"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"picture_{timestamp}.jpg"
    return handle_upload(file, filename)

# === Helper Function for Upload ===
def handle_upload(file, filename):
    local_path = os.path.join(UPLOAD_FOLDER, filename)

    if LOCAL_SAVE:
        file.save(local_path)
        print(f"Saved file locally as {local_path}")
    else:
        file_stream = file.stream.read()
        with open(local_path, 'wb') as f:
            f.write(file_stream)

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
