from flask import flash, Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key='ads'

@app.route('/', methods=['GET', 'POST'])
def panel():
    if request.method == 'POST':
        flash("Okey i'll do it")
        #ssid, key = request.form['ssid'], request.form['key']
        #try:
        #    connector.set_wifi_credentials(ssid, key)
        #    connector.connect_wifi()
        #except Exception as e:
        #    connector.disconnect_wifi()
    return render_template('panel.html', networks=["net1", "somenetwork2",
                                          "thispropablycouldbeshorter"])


@app.route('/dc')
def disconnect_wifi():
    flash("Disconnected")
    #disconnect_wifi()
    #os.remove(connector.config_file)
    return redirect(url_for('panel'))


@app.route('/health')
def health_check():
    flash("Everything OK!")
    return redirect(url_for('panel'))
