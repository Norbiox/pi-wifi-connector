#!/bin/bash

sudo apt-get install hostapd udhcpd net-tools python3-pip
pip3 install -r requirements.txt

sudo python3 configure.py

sudo systemctl unmask hostapd.service
sudo systemctl start hostapd.service
sudo systemctl enable hostapd.service
sudo systemctl start udhcpd.service
sudo systemctl enable udhcpd.service

sudo chown root:root scripts/connect.sh
sudo chmod 755 scripts/connect.sh

sudo systemctl start pi-wifi-connector.service
sudo systemctl enable pi-wifi-connector.service

sudo chmod +x task.sh
{ crontab -l; echo "* * * * * /home/pi/pi-wifi-connector/task.sh"; } | crontab -

echo "Done."
echo "Reboot device to complete installation!"
