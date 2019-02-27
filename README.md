# pi-wifi-connector
A piece of software that allows you to connect your Raspberry Pi with any wi-fi network via web browser in your smartphone or PC.

## Instalation

To install program on your Raspberry Pi please follow instructions below:

1. Enable sudo without password by editing sudoers file. Type 'sudo visudo' and add following line into the file:

        pi ALL=(ALL) NOPASSWD: ALL

2. Install software by running `setup.sh` script while being in the pi-wifi-connector directory

        ./setup.sh

3. Reboot you device

        sudo reboot

## How to use

After reboot your Raspberry Pi should automatically turn itself into hotspot mode. Then you can use your PC/smartfon/any other device with wi-fi module and web browser, and connect with Raspberry Pi. Then open browser and go to this address:

        http://192.168.0.1:8080/
        
Provide the same password as to the hotspot.
You should see a nice, intuitive, and responsive interface, that allows you to connect Raspberry Pi with available network, disconnect it (and return to hotspot mode) and check internet connection.

![alt text](https://raw.githubusercontent.com/Norbiox/pi-wifi-connector/master/images/Screenshot%20from%202019-02-27%2012-39-45.png)

### Connect device with wi-fi

To connect Raspberry Pi with wi-fi please choose your network, type in a valid password to this network and click button. After that device will try to connect with chosen wi-fi network, and you won't be able to see a result of that operation. If it succeed, Raspberry Pi will be connected to this network as long as it provides Internet connection. Otherwise Raspberry automatically turns back to hotspot mode.
NOTE: You cannot connect device to local network with no Internet connection.

### Disconnect device

To disconnect device from network and turn it back to hotspot mode, find address of device in local network (for example using `nmap`) and open it's application in browser like before:

        http://<address in local network>:8080/
        
Provide password and after that click "Go offline!" button.
