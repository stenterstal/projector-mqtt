import json
from enum import Enum

import paho.mqtt.client as mqtt

from config.config_parser import read_config, write_config
from log import Logger, LogPrefix


class MqttState(str, Enum):
    idle = 'idle'
    success = 'success',
    published = 'published'
    publish_error = 'publish_error'
    unauthorized = 'unauthorized',
    timed_out = 'timed out'

    def __str__(self) -> str:
        return self.value


class DiscoveryMqtt:
    def __init__(self):
        self.state = MqttState.idle

        # By default, we don't publish to homeassistant discovery
        self.publish = False

        # Initiate logger
        self.dash_log = Logger(LogPrefix.dashboard)

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect

    def start(self, publish=False):
        # Shall we publish to homeassistant discovery on connect?
        self.publish = publish
        # Get the latest mqtt config
        config = read_config().get('mqtt')
        # Initialize client with latest config
        self.mqttc.username_pw_set(config["user"], config["password"])
        try:
            self.dash_log.info("Test MQTT client config")
            # Connect
            self.mqttc.connect(config["address"], int(config["port"]), 60)
            self.mqttc.loop_start()
        except TimeoutError as e:
            self.state = MqttState.timed_out
            self.dash_log.error("Timed out trying to connect to " + config["address"] + ":" + config["port"])
            self.set_config_is_valid(False)

    def close(self):
        self.dash_log.info("Shutting down MQTT client after connection test")
        self.mqttc.loop_stop()
        self.mqttc.disconnect()
        # Unset publish to homeassistant discovery
        self.publish = False

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != "Success":
            self.dash_log.error(f"Something went wrong connecting to MQTT with reason: {reason_code}")
            if reason_code == "Not authorized":
                self.state = MqttState.unauthorized
            self.set_config_is_valid(False)
        else:
            self.state = MqttState.success
            self.set_config_is_valid(True)
            self.dash_log.info("Successful connection test to MQTT")
            if self.publish:
                self.homeassistant_discovery()

        self.close()

    def homeassistant_discovery(self):
        homeassistant_id = read_config().get('homeassistant').get('id')
        # Failsafe
        if homeassistant_id is None:
            self.state = MqttState.publish_error
            return
        discovery_message = self.discovery_message(homeassistant_id)
        json_message = json.dumps(discovery_message)
        self.mqttc.publish("homeassistant/device/%s/config" % homeassistant_id, json_message, qos=1)
        self.dash_log.info("Published config to home assistant autodiscovery MQTT")
        self.state = MqttState.published

    @staticmethod
    def set_config_is_valid(valid: bool):
        write_config('config', dict({'valid': valid}))

    @staticmethod
    def discovery_message(homeassistant_id):
        return {
            "device": {
                "name": "DLP Projector",
                "ids": homeassistant_id,
                "manufacturer": "Texas Instruments / Beaglebone",
                "model": "DLPDLCR2000EVM"
            },
            "origin": {
                "name": "Sten ter Stal"
            },
            "components": {
                "projector": {
                    "platform": "switch",
                    "unique_id": homeassistant_id,
                    "name": "Projector",
                    "icon": "mdi:projector"
                }
            },
            "command_topic": "dlp-projector/"+homeassistant_id+"/set",
            "state_topic": "dlp-projector/"+homeassistant_id+"/set"
        }