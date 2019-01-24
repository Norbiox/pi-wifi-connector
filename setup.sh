#!/bin/bash

sudo apt-get install hostapd udhcpd net-tools python3-pip
pip3 install -r requirements.txt

sudo cp conf/udhcpd.conf /etc/udhcpd.conf
sudo cp conf/udhcpd /etc/default/udhcpd
sudo cp conf/interfaces /etc/default/interfaces
sudo cp conf/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp conf/hostapd /etc/default/hostapd

sudo systemctl unmask hostapd.service
sudo systemctl start hostapd.service
sudo systemctl enable hostapd.service
sudo systemctl start udhcpd.service
sudo systemctl enable udhcpd.service
