import paho.mqtt.client as mqtt

from config import config_parser
from log import Logger, LogPrefix
from projector.lightcrafter.constants import SlaveAddr, IODebug
from projector.lightcrafter.dpp2607 import *

# Set in config file
MQTT_DEVICE_ID = "912f98b36b4f4776b785210671a78e5e"


class Projector:
    def __init__(self):
        self.config = config_parser.read_config()

        # Initiate logger
        self.mqtt_log = Logger(LogPrefix.mqtt)
        self.proj_log = Logger(LogPrefix.projector)

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.username_pw_set(self.config["mqtt_user"], self.config["mqtt_password"])

        self.mqttc.connect(self.config["mqtt_address"], int(self.config["mqtt_port"]), 60)

        self.mqttc.loop_forever()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != "Success":
            self.mqtt_log.error(f"Something went wrong: Connected with result code {reason_code}")
        else:
            self.mqtt_log.info("Successfully connected")

        client.subscribe("homeassistant/switch/%s/#" % MQTT_DEVICE_ID)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        if msg.topic == "homeassistant/switch/%s/set" % MQTT_DEVICE_ID:
            if payload == "ON":
                self.mqtt_log.info("Received turn on")
                self.projector_turn_on()
            elif payload == "OFF":
                self.mqtt_log.info("Received turn off")
                self.projector_turn_off()

    def projector_turn_on(self):
        DPP2607_Open()
        DPP2607_SetSlaveAddr(SlaveAddr)
        DPP2607_SetIODebug(IODebug)
        DPP2607_Write_LedCurrentRed(255)
        DPP2607_Write_LedCurrentGreen(255)
        DPP2607_Write_LedCurrentBlue(255)
        DPP2607_Write_PropagateLedCurrents(1)
        DPP2607_Close()
        self.proj_log.info("Set screen brightness to 255 (turn-on)")

    def projector_turn_off(self):
        DPP2607_Open()
        DPP2607_SetSlaveAddr(SlaveAddr)
        DPP2607_SetIODebug(IODebug)
        DPP2607_Write_LedCurrentRed(0)
        DPP2607_Write_LedCurrentGreen(0)
        DPP2607_Write_LedCurrentBlue(0)
        DPP2607_Write_PropagateLedCurrents(1)
        DPP2607_Close()
        self.proj_log.info("Set screen brightness to 0 (turn-off)")