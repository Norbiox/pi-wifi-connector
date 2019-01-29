#!/bin/bash

sudo killall wpa_supplicant
sudo killall dhclient
sudo ip addr flush dev wlan0
sudo ifconfig wlan0 down
sudo ifconfig wlan0 up
sudo /etc/init.d/networking restart
sudo systemctl restart hostapd.service
