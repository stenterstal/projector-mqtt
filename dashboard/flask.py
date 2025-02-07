import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify

from config.config_parser import write_config, read_config
from dashboard.mqtt_discovery import DiscoveryMqtt

app = Flask(__name__)

mqtt = DiscoveryMqtt()

app.secret_key = "9@jhqLMTf0KKqSS%p_cAN~dG'%(fzQZV%ex1o)&BQ*hHe08g!p&ByQng3t~_QoB"

@app.route("/")
def page_mqtt():
    data = read_config().get('mqtt')
    status = mqtt.state
    return render_template('index.html', data=data, status=status)

@app.route("/homeassistant")
def page_homeassistant():
    data = read_config().get('homeassistant')
    status = mqtt.state
    return render_template('homeassistant.html', data=data, status=status)

@app.route("/config/mqtt", methods=['POST'])
def config_mqtt():
    data = {
        'address': request.form['address'],
        'port': request.form['port'],
        'user': request.form['user'],
        'password': request.form['password'],
    }
    write_config("mqtt", data)
    mqtt.start()
    return redirect(url_for('page_mqtt'))

@app.route("/publish", methods=['POST'])
def config_homeassistant():
    data = {
        'id': request.form['id'],
        'command_topic': request.form['command_topic'].replace('<id>', request.form['id']),
        'state_topic': request.form['state_topic'].replace('<id>', request.form['id'])
    }
    write_config("homeassistant", data)
    mqtt.start(publish=True)
    return redirect(url_for('page_homeassistant'))

@app.route("/display")
def display():
    return render_template('display.html')

# FOR TESTING ONLY!
@app.route("/disruptions")
def disruptions():
    from app import ROOT_DIR
    with open(os.path.join(ROOT_DIR, 'disruptions.json'), 'r') as file:
        data = json.load(file)  # Load the JSON content from the file
    return jsonify(data)  # Return the JSON data as a response
