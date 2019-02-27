SECRET_KEY = 'super-duper-not-hackable-at-all-key'
WPA_CONFIG_FILE = '/home/pi/wifi_credentials.conf'
WPA_STATUS_FILE = '/home/pi/wpa_logs.txt'

hostapd_file = '/etc/hostapd/hostapd.conf'
with open(hostapd_file) as f:
    for line in f.readlines():
        m = re.match(r'(?:wpa_passphrase=)(.+)', line)
        if m:
            HOTSPOT_PASSWORD = m.group(1)
            break
    else:
        raise ValueError("Couldn't find hotspot password in {}".format(
                         hostapd_file))
