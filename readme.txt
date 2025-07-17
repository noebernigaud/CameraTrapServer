LXC container automatically runs the start_ser.sh with this systemd file
/etc/systemd/system/esp32server.service

** See logs for the server on LXC container **
journalctl -u esp32server -f

** Create an LXC container on proxmox **
- Create the LXC container, don't forget to give it network access (DHCP)
- Run the commands:
    - apt update && apt upgrade -y
    - apt install -y python3 python3-pip git
    - mkdir /opt/esp32-video-server
    - cd mkdir /opt/esp32-video-server
    - git clone https://github.com/yourname/esp32-video-server.git /opt/esp32-video-server
    - python3 -m venv venv
    - nano /etc/systemd/system/esp32server.service
-> 
[Unit]
Description=ESP32 Video Upload Server
After=network.target

[Service]
ExecStart=/opt/esp32-video-server/run.sh
WorkingDirectory=/opt/esp32-video-server
Restart=always
User=root

[Install]
WantedBy=multi-user.target
    - systemctl daemon-reexec
    - systemctl enable esp32server
    - systemctl start esp32server