import json

import paho.mqtt.client as mqtt

from config import config_parser
from log import Logger, LogPrefix
from payloads.discovery import make_discovery_message


# Set in config file
MQTT_DEVICE_ID = "912f98b36b4f4776b785210671a78e5e"


class DashboardMqtt:
    def __init__(self):
        self.config = config_parser.read_config()

        # Initiate logger
        self.dash_log = Logger(LogPrefix.dashboard)

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.username_pw_set(self.config["mqtt_user"], self.config["mqtt_password"])

        self.mqttc.connect(self.config["mqtt_address"], int(self.config["mqtt_port"]), 60)

        # No loop_forever as its blocking
        self.mqttc.loop_start()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != "Success":
            self.dash_log.error(f"Something went wrong connecting to MQTT: Connected with result code {reason_code}")
        else:
            self.dash_log.info("Successfully connected to MQTT")

        if self.config['mqtt_autodiscovery'] == 'true':
            self.homeassistant_discovery()

        client.subscribe("homeassistant/switch/%s/#" % MQTT_DEVICE_ID)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        if msg.topic == "homeassistant/switch/%s/set" % MQTT_DEVICE_ID:
            if payload == "ON":
                self.dash_log.info("Received MQTT turn on")
                # Reload homepage if on homepage
            elif payload == "OFF":
                self.dash_log.info("Received MQTT turn off")
                # Reload homepage if on homepage

    def homeassistant_discovery(self):
        discovery_message = make_discovery_message(MQTT_DEVICE_ID)
        string = json.dumps(discovery_message)

        self.mqttc.publish("homeassistant/device/%s/config" % MQTT_DEVICE_ID, string, qos=1)
        print("[MQTT] Published config to home assistant autodiscovery")
