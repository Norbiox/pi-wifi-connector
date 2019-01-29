#!/bin/bash

echo "disconnecting from network ..."
sudo killall wpa_supplicant
sudo killall dhclient

echo "resetting interface ..."
sudo ip addr flush dev wlan0
sudo ifconfig wlan0 down
sudo ifconfig wlan0 up

echo "restarting hostapd ..."
sudo /etc/init.d/networking restart
sudo systemctl restart hostapd.service

echo "Hotspot Mode activated"
