#!/usr/bin/python3
import os
from time import sleep

from flask import flash, Flask, redirect, render_template, request, url_for

from .lib import WifiConnector


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = os.getenv('SECRET_KEY')

connector = WifiConnector(
    app.config['WPA_CONFIG_FILE'],
    app.config['WPA_STATUS_FILE'],
    autoconnect=True
)


@app.route('/', methods=['GET', 'POST'])
def panel():
    if request.method == 'POST':
        ssid, key = request.form['ssid'], request.form['password']
        try:
            connector.set_wifi_credentials(ssid, key)
            connector.connect_wifi()
        except Exception as e:
            print(e)
            connector.disconnect_wifi()
    return render_template('panel.html',
                           networks=connector.get_available_networks())


@app.route('/dc')
def disconnect_wifi():
    connector.disconnect_wifi(remove_saved_credentials=True)
    return redirect(url_for('panel'))


@app.route('/health')
def health_check():
    if connector.is_online():
        flash("Device is online!")
    else:
        flash("Device is offline")
    return redirect(url_for('panel'))


@app.route('/dc_if_offline')
def disconnect_if_offline():
    i = 0
    while i < 3:
        if connector.get_current_ip() == '192.168.0.1':
            break
        elif connector.is_online():
            return 'ONLINE'
        elif i < 2:
            sleep(2)
        else:
            connector.disconnect_wifi()
        i += 1
    return 'HOTSPOT_MODE'
