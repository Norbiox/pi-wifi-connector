#!/bin/bash

WPA_CONFIG_FILE=$1
WPA_STATUS_FILE=$2

echo "Stopping Hotspot Mode ..."
sudo systemctl stop hostapd.service
sudo ifconfig wlan0 up
sudo ip addr flush dev wlan0
sudo truncate -s 0 $WPA_STATUS_FILE

echo "Trying to connect with wi-fi network ..."
sudo wpa_supplicant -B \
    -D wext \
    -i wlan0 \
    -f $WPA_STATUS_FILE \
    -c $WPA_CONFIG_FILE

declare -i i=0
declare -i timeout=15

while [ $i -le $timeout ]; do
    if grep -iq 'CTRL-EVENT-CONNECTED' $WPA_STATUS_FILE; then
        echo "Device has been connected! Obtaining IP address ..."
        sudo dhclient wlan0
        exit 0
    elif grep -iq '4-Way Handshake failed' $WPA_STATUS_FILE; then
        echo "Device couldn't connect with network"
        exit 1
    fi

    (( i++ ))
    sleep 1
done

