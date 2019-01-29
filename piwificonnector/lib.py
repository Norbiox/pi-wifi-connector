#!/usr/bin python3
import netifaces as ni
import re
from getpass import getpass
from pathlib import Path
from subprocess import run, PIPE
from urllib.request import urlopen


class BashScriptError(Exception):
    pass


class WifiConnector:

    def __init__(self, wpa_config_file, wpa_status_file, autoswitch=False):
        self.config_file = Path(wpa_config_file)
        self.status_file = Path(wpa_status_file)
        self.status_file.touch()
        if autoswitch and self.config_file.exists():
            try:
                self.connect_wifi()
            except BashScriptError:
                self.disconnect_wifi()

    @classmethod
    def is_online(cls):
        for i in range(3):
            try:
                urlopen("https://google.com")
                return True
            except Exception as e:
                continue
        return False

    @classmethod
    def get_available_networks(cls):
        output = run("sudo -E scripts/scan.sh".split(), stdout=PIPE,
                     stderr=PIPE)
        results = output.stdout.decode("utf-8").split("\n")
        ssids = []
        for m in [re.search(r'ESSID:\"(?P<name>.+)\"', r) for r in results]:
            try:
                ssids.append(m.group('name'))
            except Exception as e:
                pass
        return ssids

    @classmethod
    def get_current_ip(cls, interface='wlan0'):
        ni.ifaddresses(interface)
        return ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

    def connect_wifi(self):
        config_file_path = str(self.config_file.resolve())
        if not self.config_file.exists():
            raise FileNotFoundError("WPA config file not found at {}".format(
                config_file_path
            ))
        self.disconnect_wifi()
        cmd = "sudo -E scripts/connect.sh '{}' '{}'".format(
            config_file_path, str(self.status_file.resolve())
        )
        output = run(cmd.split())
        if not output.returncode:
            return 0
        raise BashScriptError("An error occured when run connect.sh")

    def disconnect_wifi(self):
        output = run("sudo -E scripts/disconnect.sh".split())
        if not output.returncode:
            return 0
        raise BashScriptError("An error occured when run disconnect.sh")

    def set_wifi_credentials(self, ssid: str, key: str):
        if not 8 <= len(key) <= 63:
            raise ValueError("Key length must be from 8 to 63")
        output = run(['wpa_passphrase', ssid, key], stdout=PIPE)
        config_string = output.stdout.decode("utf-8")
        if "\n" not in config_string:
            raise Exception(
                "wpa_passphrase couldn't generate proper configuration, " +
                "check entered network credentials"
            )
        with open(self.config_file, 'w+') as f:
            f.write(config_string)


if __name__ == '__main__':
    wc = WifiConnector('test.conf', 'test.txt')
    ssids = wc.get_available_networks()
    print("Avaiable wi-fi access points:")
    print('\n'.join(ssids))
    ssid = input("Provide networks ssid: ")
    key = getpass()
    wc.set_wifi_credentials(ssid, key)
    wc.connect_wifi()
    input("You're connected with wifi. Press [ENTER] to disconnect.")
    wc.disconnect_wifi()
    os.remove('test.conf')
    os.remove('test.txt')
