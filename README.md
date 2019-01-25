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
