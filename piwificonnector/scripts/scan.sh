#!/bin/bash

echo "Scanning available networks ..."
sudo iwlist wlan0 scan | grep ESSID
