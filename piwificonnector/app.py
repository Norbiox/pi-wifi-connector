#!/usr/bin/python3
import os
from time import sleep
from functools import wraps

from flask import (flash, Flask, make_response, redirect, render_template,
                   request, session, url_for)

from .lib import WifiConnector


class AuthenticationError(Exception):
    pass


app = Flask(__name__)
app.config.from_pyfile('config.py')

connector = WifiConnector(
    app.config['WPA_CONFIG_FILE'],
    app.config['WPA_STATUS_FILE'],
    autoconnect=True
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            logged_in = session['logged_in']
            if logged_in is not True:
                raise AuthenticationError('User not logged in')
        except (KeyError, AuthenticationError) as e:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = make_response(redirect(url_for('panel')))
        if request.form['password'] == app.config['HOTSPOT_PASSWORD']:
            session['logged_in'] = True
        return response
    else:
        return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def panel():
    if request.method == 'POST':
        ssid, key = request.form['ssid'], request.form['password']
        try:
            connector.set_wifi_credentials(ssid, key)
            connector.connect_wifi()
        except Exception as e:
            print(e)
            connector.disconnect_wifi()
    return render_template('manage.html',
                           networks=connector.get_available_networks())


@app.route('/dc')
@login_required
def disconnect_wifi():
    connector.disconnect_wifi(remove_saved_credentials=True)
    return redirect(url_for('panel'))


@app.route('/health')
@login_required
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
