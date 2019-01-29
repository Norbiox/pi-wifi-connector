#!/usr/bin/python3
import os

from flask import flash, Flask, redirect, render_template, request, url_for

from .lib import WifiConnector


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = os.getenv('SECRET_KEY')

connector = WifiConnector(
    app.config['WPA_CONFIG_FILE'],
    app.config['WPA_STATUS_FILE'],
    autoswitch=True
)


@app.route('/', methods=['GET', 'POST'])
def panel():
    if request.method == 'POST':
        ssid, key = request.form['ssid'], request.form['password']
        try:
            connector.set_wifi_credentials(ssid, key)
            connector.connect_wifi()
        except Exception as e:
            connector.disconnect_wifi()
    return render_template('panel.html',
                           networks=connector.get_available_networks())


@app.route('/dc')
def disconnect_wifi():
    disconnect_wifi()
    os.remove(connector.config_file)
    return redirect(url_for('panel'))


@app.route('/health')
def health_check():
    flash("Everything OK!")
    return redirect(url_for('panel'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, use_reloader=False)
