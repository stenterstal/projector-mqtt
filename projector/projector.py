import subprocess
from enum import Enum

from projector.lightcrafter.dpp2607 import *
from projector.lightcrafter.constants import SlaveAddr, IODebug


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
            self.turn_on()
        else:
            self.turn_off()

    def turn_on(self):
        DPP2607_Open()
        DPP2607_SetSlaveAddr(SlaveAddr)
        DPP2607_SetIODebug(IODebug)
        DPP2607_Write_LedCurrentRed(255)
        DPP2607_Write_LedCurrentGreen(255)
        DPP2607_Write_LedCurrentBlue(255)
        DPP2607_Write_PropagateLedCurrents(1)
        DPP2607_Close()

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