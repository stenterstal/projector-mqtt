import os
import subprocess
import time

import paho.mqtt.client as mqtt
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from watchdog.observers import Observer

from config import config_parser
from config.config_parser import validate_config
from log import Logger, LogPrefix
from projector.lightcrafter.constants import SlaveAddr, IODebug
from projector.lightcrafter.dpp2607 import *

class Projector:
    def __init__(self):
        # Initiate logger
        self.mqtt_log = Logger(LogPrefix.mqtt)
        self.proj_log = Logger(LogPrefix.projector)

        # Read and check config
        config = config_parser.read_config()

        errors = validate_config()
        if len(errors) > 0:
            self.proj_log.error("Not starting projector, config.ini incomplete")
            return

        self.mqtt_topic = config['homeassistant']['command_topic']
        self.mqtt_state_topic = config['homeassistant']['state_topic']

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.username_pw_set(config['mqtt']["user"], config['mqtt']["password"])

        self.mqttc.connect(config['mqtt']["address"], int(config['mqtt']["port"]), 60)

        self.mqttc.loop_forever()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != "Success":
            self.mqtt_log.error(f"Something went wrong: Connected with result code {reason_code}")
        else:
            self.mqtt_log.info("Successfully connected")
            self.mqttc.publish(self.mqtt_state_topic, "ON")

        client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        if msg.topic == self.mqtt_topic:
            if payload == "ON":
                self.mqtt_log.info("Received turn on")
                # Reload frontend
                subprocess.run(["/usr/bin/sudo", "xdotool", "key", "ctrl+r"])
                # Give frontend some time to (re)load
                # (After the frontend receives a reload keypress, it will fade in over the course of 3 seconds)
                time.sleep(2)
                # Then turn on the actual screen
                self.projector_turn_on()
            elif payload == "OFF":
                self.mqtt_log.info("Received turn off")
                self.projector_turn_off()

    def projector_turn_on(self):
        DPP2607_Open()
        DPP2607_SetSlaveAddr(SlaveAddr)
        DPP2607_SetIODebug(IODebug)
        DPP2607_Write_VideoSourceSelection(SourceSel.EXTERNAL_VIDEO_PARALLEL_I_F_)
        DPP2607_Write_VideoResolution(Resolution.WVGA_864_LANDSCAPE) #640x360
        DPP2607_Write_LedCurrentRed(300)
        DPP2607_Write_LedCurrentGreen(300)
        DPP2607_Write_LedCurrentBlue(300)
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