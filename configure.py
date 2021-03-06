#!/usr/bin/env python3
from getpass import getpass


HOSTAPD_CONF = {
    'path': '/etc/hostapd/hostapd.conf',
    'content': '\n'.join([
        "interface=wlan0",
        "driver=nl80211",
        "ssid={ssid}",
        "hw_mode=g",
        "channel=7",
        "macaddr_acl=0",
        "auth_algs=1",
        "ignore_broadcast_ssid=0",
        "wpa=2",
        "wpa_passphrase={passphrase}",
        "wpa_key_mgmt=WPA-PSK",
        "wpa_pairwise=TKIP",
        "rsn_pairwise=CCMP"
    ])
}


HOSTAPD = {
    'path': '/etc/default/hostapd',
    'content': 'DAEMON_CONF="/etc/hostapd/hostapd.conf"'
}


UDHCPD_CONF = {
    'path': '/etc/udhcpd.conf',
    'content': """# The start and end of the IP lease block

start           192.168.0.2     #default: 192.168.0.20
end             192.168.0.254    #default: 192.168.0.254


# The interface that udhcpd will use

interface       wlan0           #default: eth0


# The maximim number of leases (includes addressesd reserved
# by OFFER's, DECLINE's, and ARP conficts

#max_leases     254             #default: 254


# If remaining is true (default), udhcpd will store the time
# remaining for each lease in the udhcpd leases file. This is
# for embedded systems that cannot keep time between reboots.
# If you set remaining to no, the absolute time that the lease
# expires at will be stored in the dhcpd.leases file.

remaining       yes             #default: yes


# The time period at which udhcpd will write out a dhcpd.leases
# file. If this is 0, udhcpd will never automatically write a
# lease file. (specified in seconds)

#auto_time      7200            #default: 7200 (2 hours)


# The amount of time that an IP will be reserved (leased) for if a
# DHCP decline message is received (seconds).

#decline_time   3600            #default: 3600 (1 hour)


# The amount of time that an IP will be reserved (leased) for if an
# ARP conflct occurs. (seconds

#conflict_time  3600            #default: 3600 (1 hour)


# How long an offered address is reserved (leased) in seconds

#offer_time     60              #default: 60 (1 minute)

# If a lease to be given is below this value, the full lease time is
# instead used (seconds).

#min_lease      60              #defult: 60


# The location of the leases file

#lease_file     /var/lib/misc/udhcpd.leases     #defualt: /var/lib/misc/udhcpd.leases

# The location of the pid file
#pidfile        /var/run/udhcpd.pid     #default: /var/run/udhcpd.pid

# Everytime udhcpd writes a leases file, the below script will be called.
# Useful for writing the lease file to flash every few hours.

#notify_file                            #default: (no script)

#notify_file    dumpleases      # <--- usefull for debugging

# The following are bootp specific options, setable by udhcpd.

#siaddr         192.168.0.22            #default: 0.0.0.0

#sname          zorak                   #default: (none)

#boot_file      /var/nfs_root           #default: (none)

# The remainer of options are DHCP options and can be specifed with the
# keyword 'opt' or 'option'. If an option can take multiple items, such
# as the dns option, they can be listed on the same line, or multiple
# lines. The only option with a default is 'lease'.

#Examles
opt     dns     8.8.8.8 4.2.2.2
option  subnet  255.255.255.0
opt     router  192.168.0.1
opt     wins    192.168.10.10
option  dns     129.219.13.81   # appened to above DNS servers for a total of 3
option  domain  local
option  lease   864000          # 10 days of seconds"""
}


UDHCPD = {
    'path': '/etc/default/udhcpd',
    'content': '#DHCPD_ENABLED="no"\nDHCPD_OPTS="-S"'
}


INTERFACES = {
    'path': '/etc/network/interfaces',
    'content': '\n'.join([
        "auto wlan0",
        "iface wlan0 inet static",
        "  address 192.168.0.1",
        "  netmask 255.255.255.0"
    ])
}


APP_SERVICE = {
    'path': '/lib/systemd/system/pi-wifi-connector.service',
    'content': '\n'.join([
        "[Unit]",
        "Description=pi-wifi-connector application service\n",
        "[Service]",
        "User=pi",
        "Restart=always",
        "ExecStart=/bin/bash -c '../run.sh'",
        "WorkingDirectory=/home/pi/pi-wifi-connector/piwificonnector",
        "RemainAfterExit=yes\n",
        "[Install]",
        "WantedBy=multi-user.target"
    ])
}


print("Please provide hotspot configuration")

ssid = input("SSID of hotspot network: ")
while not ssid:
    print("SSID cannot be empty string!")
    ssid = input("SSID of hotspot network: ")

passphrase = ""
while not passphrase:
    passphrase = getpass("Password to hotspot network: ")
    if len(passphrase) < 8 or len(passphrase) > 63:
        passphrase = ""
        print("Password must contain between 8 and 63 characters")
        continue
    passphrase_repeated = getpass("Repeat password: ")
    if passphrase != passphrase_repeated:
        passphrase = ""
        print("Given passwords are not the same!")
        continue
    else:
        break


print("Writing configuration files")
print("hostapd...")
with open(HOSTAPD_CONF['path'], 'w+') as f:
    f.write(HOSTAPD_CONF['content'].format(ssid=ssid, passphrase=passphrase))
with open(HOSTAPD['path'], 'w+') as f:
    f.write(HOSTAPD['content'])

print("udhcpd...")
with open(UDHCPD_CONF['path'], 'w+') as f:
    f.write(UDHCPD_CONF['content'])
with open(UDHCPD['path'], 'w+') as f:
    f.write(UDHCPD['content'])

print("interfaces...")
with open(INTERFACES['path'], 'w+') as f:
    f.write(INTERFACES['content'])

print("app service...")
with open(APP_SERVICE['path'], 'w+') as f:
    f.write(APP_SERVICE['content'])

print("Done.")
