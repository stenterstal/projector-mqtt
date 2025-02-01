import subprocess

from flask import Flask, render_template, request, redirect, url_for, session, g

from config_parser import write_config, read_config
from mqtt.mqtt_handler import Mqtt
from projector.projector import Projector

app = Flask(__name__)

projector = Projector()

mqtt = Mqtt()

app.secret_key = "9@jhqLMTf0KKqSS%p_cAN~dG'%(fzQZV%ex1o)&BQ*hHe08g!p&ByQng3t~_QoB"

@app.route("/")
def page_dashboard():
    projector_state = projector.state
    return render_template('index.html', projector_state=projector_state)

@app.route("/projector/toggle")
def projector_toggle():
    projector.toggle()
    return redirect('/')

@app.route("/mqtt")
def page_mqtt():
    data = read_config()
    status = None
    if 'status' in session.keys():
        status = session['status']
        session.pop('status')
    return render_template('mqtt.html', data=data, status=status)


@app.route("/config", methods=['POST'])
def config():
    data = {
        'mqtt_address': request.form['mqtt_address'],
        'mqtt_port': request.form['mqtt_port'],
        'mqtt_user': request.form['mqtt_user'],
        'mqtt_password': request.form['mqtt_password'],
        'mqtt_autodiscovery': 'true' if request.form.get('mqtt_autodiscovery') else 'false'
    }
    write_config(data)
    session["status"] = "success_save"
    return redirect(url_for('page_mqtt'))