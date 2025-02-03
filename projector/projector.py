import json

import paho.mqtt.client as mqtt

from config import config_parser
from payloads.discovery import make_discovery_message
from projector.lightcrafter.dpp2607 import *
from projector.lightcrafter.constants import SlaveAddr, IODebug

MQTT_DEVICE_ID = "912f98b36b4f4776b785210671a78e5e"


class Projector:
    def __init__(self):
        self.config = config_parser.read_config()

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.username_pw_set(self.config["mqtt_user"], self.config["mqtt_password"])

        self.mqttc.connect(self.config["mqtt_address"], int(self.config["mqtt_port"]), 60)

        self.mqttc.loop_forever()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != "Success":
            print(f"[MQTT] Something went wrong: Connected with result code {reason_code}")
        else:
            print("[MQTT] Successfully connected")

        if self.config['mqtt_autodiscovery'] == 'true':
            self.homeassistant_discovery()

        client.subscribe("homeassistant/switch/%s/#" % MQTT_DEVICE_ID)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        if msg.topic == "homeassistant/switch/%s/set" % MQTT_DEVICE_ID:
            if payload == "ON":
                print("[MQTT] Received turn on")
                projector_turn_on()
            elif payload == "OFF":
                print("[MQTT] Received turn off")
                projector_turn_off()

    def homeassistant_discovery(self):
        discovery_message = make_discovery_message(MQTT_DEVICE_ID)
        string = json.dumps(discovery_message)

        self.mqttc.publish("homeassistant/device/%s/config" % MQTT_DEVICE_ID, string, qos=1)
        print("[MQTT] Published config to home assistant autodiscovery")

#
#   (STATIC) Projector i2c functions
#

def projector_turn_on():
    DPP2607_Open()
    DPP2607_SetSlaveAddr(SlaveAddr)
    DPP2607_SetIODebug(IODebug)
    DPP2607_Write_LedCurrentRed(255)
    DPP2607_Write_LedCurrentGreen(255)
    DPP2607_Write_LedCurrentBlue(255)
    DPP2607_Write_PropagateLedCurrents(1)
    DPP2607_Close()
    print('[PROJ] Set screen brightness to 255 (turn-on)')

def projector_turn_off():
    DPP2607_Open()
    DPP2607_SetSlaveAddr(SlaveAddr)
    DPP2607_SetIODebug(IODebug)
    DPP2607_Write_LedCurrentRed(0)
    DPP2607_Write_LedCurrentGreen(0)
    DPP2607_Write_LedCurrentBlue(0)
    DPP2607_Write_PropagateLedCurrents(1)
    DPP2607_Close()
    print('[PROJ] Set screen brightness to 0 (turn-off)')