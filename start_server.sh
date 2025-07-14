#!/bin/bash

cd /opt/esp32-video-server

# Pull latest updates
git pull

# Activate virtualenv
source venv/bin/activate

# Update/install dependencies
pip install -r requirements.txt

# Run the server (adjust the command if needed)
python app.py
