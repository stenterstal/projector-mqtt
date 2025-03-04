import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify

from config.config_parser import write_config, read_config
from dashboard.mqtt_discovery import DiscoveryMqtt

app = Flask(__name__)

mqtt = DiscoveryMqtt()

app.secret_key = "9@jhqLMTf0KKqSS%p_cAN~dG'%(fzQZV%ex1o)&BQ*hHe08g!p&ByQng3t~_QoB"

#
#   Default route
#   - Redirects to the first tab of the config screen
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('config_page_mqtt'))

#
#   Projector Display
#
@app.route("/display")
def display():
    environment = {}
    config = read_config().get('display')
    if config:
        # NS Environment variables
        environment['ns_enabled'] = config.get('ns_enabled') == 'True'
        environment['ns_api_key'] = config.get('ns_api_key')
        environment['ns_station_code'] = config.get('ns_station_code')
        # Weather Environment variables
        environment['weather_enabled'] = config.get('weather_enabled') == 'True'
        environment['weather_latitude'] = config.get('weather_latitude')
        environment['weather_longitude'] = config.get('weather_longitude')
    return render_template('display.html', environment=environment)

#
#   Config MQTT
#
@app.route("/config/mqtt", methods=['GET'])
def config_page_mqtt():
    data = read_config().get('mqtt')
    status = mqtt.state
    return render_template('config_mqtt.html', data=data, status=status)
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
    return redirect(url_for('config_page_mqtt'))

#
#   Config Homeassistant
#
@app.route("/config/homeassistant", methods=['GET'])
def config_page_homeassistant():
    data = read_config().get('homeassistant')
    status = mqtt.state
    return render_template('config_homeassistant.html', data=data, status=status)

@app.route("/config/homeassistant", methods=['POST'])
def config_homeassistant():
    data = {
        'id': request.form['id'],
        'command_topic': request.form['command_topic'].replace('<id>', request.form['id']),
        'state_topic': request.form['state_topic'].replace('<id>', request.form['id'])
    }
    write_config("homeassistant", data)
    mqtt.start(publish=True)
    return redirect(url_for('config_page_homeassistant'))

#
#   Config Display
#
@app.route("/config/display", methods=['GET'])
def config_page_display():
    data = read_config().get('display')
    return render_template('config_display.html', data=data)

@app.route("/config/display", methods=['POST'])
def config_display():
    data = {
        'ns_enabled': request.form.get('ns_enabled') and request.form['ns_enabled'] == 'on' or False,
        'ns_api_key': request.form['ns_api_key'],
        'ns_station_code': request.form['ns_station_code'],
        'weather_enabled': request.form.get('weather_enabled') and request.form['weather_enabled'] == 'on' or False,
        'weather_latitude': request.form['weather_latitude'],
        'weather_longitude': request.form['weather_longitude'],
    }
    write_config("display", data)
    return redirect(url_for('config_page_display'))


#
#   TESTING: Api route
#

# FOR TESTING ONLY!
@app.route("/test/disruptions")
def disruptions():
    from app import ROOT_DIR
    with open(os.path.join(ROOT_DIR, 'dashboard/test/disruptions.json'), 'r') as file:
        data = json.load(file)  # Load the JSON content from the file
    return jsonify(data)  # Return the JSON data as a response
@app.route("/test/weather")
def weather():
    from app import ROOT_DIR
    with open(os.path.join(ROOT_DIR, 'dashboard/test/weather.json'), 'r') as file:
        data = json.load(file)  # Load the JSON content from the file
    return jsonify(data)  # Return the JSON data as a response

