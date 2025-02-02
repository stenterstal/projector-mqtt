import subprocess
from enum import Enum

from lightcrafter.dpp2607 import *
from lightcrafter.constants import SlaveAddr, IODebug


class ProjectorState(str, Enum):
    stopped = 'stopped'
    running = 'running'

    def __str__(self) -> str:
        return self.value

class Projector:
    def __init__(self):
        self.state = ProjectorState('stopped')

    def toggle(self) -> bool:
        if self.state == ProjectorState.stopped:
            return self.turn_on()
        else:
            return self.turn_off()

    def turn_on(self) -> bool:
        if self.state == ProjectorState.stopped:
            command = "echo 1 > /sys/class/gpio/gpio48/value"
            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if not error:
                self.state = ProjectorState('running')
                print("[PROJ] Turned on")
                return True
            print("[PROJ] Something went wrong trying to turn on projector")
        return False

    def turn_off(self):
        DPP2607_Open()
        DPP2607_SetSlaveAddr(SlaveAddr)
        DPP2607_SetIODebug(IODebug)
        DPP2607_Write_LedCurrentRed(0)
        DPP2607_Write_LedCurrentGreen(0)
        DPP2607_Write_LedCurrentBlue(0)
        DPP2607_Write_PropagateLedCurrents(1)
        DPP2607_Close()

    def __getstate__(self) -> ProjectorState:
        return self.state