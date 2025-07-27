# app.py
from flask import Flask
from routes.health_routes import health_bp
from routes.video_routes import video_bp
from routes.picture_routes import picture_bp
from routes.mjpeg_routes import mjpeg_bp
import os
from constants.constants import UPLOAD_FOLDER

app = Flask(__name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(health_bp)
app.register_blueprint(video_bp)
app.register_blueprint(picture_bp)
app.register_blueprint(mjpeg_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
