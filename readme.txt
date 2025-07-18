LXC container automatically runs the start_ser.sh with this systemd file
/etc/systemd/system/esp32server.service

** See logs for the server on LXC container **
journalctl -u esp32server -f

** Create an LXC container on proxmox **
- Create the LXC container, don't forget to give it network access (DHCP)
- Run the commands:
    - apt update && apt upgrade -y
    - apt install -y python3 python3-pip python3.12-venv git 
    - mkdir /opt/esp32-video-server
    - cd /opt/esp32-video-server
    - git clone https://github.com/noebernigaud/CameraTrapServer /opt/esp32-video-server
    - python3 -m venv venv
    - nano /etc/systemd/system/esp32server.service
-> 
[Unit]
Description=ESP32 Video Python Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/esp32-video-server
ExecStart=/bin/bash /opt/esp32-video-server/start_server.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
<-

    - systemctl daemon-reexec
    - systemctl enable esp32server
    - systemctl start esp32server

After this configuration, the server will automaticaly launch on container start with latest code on github.
Check the log to get the ip adress and change it in the client if needed.