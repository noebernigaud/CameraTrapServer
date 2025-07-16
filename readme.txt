LXC container automatically runs the start_ser.sh with this systemd file
/etc/systemd/system/esp32server.service

** See logs for the server on LXC container **
journalctl -u esp32server -f