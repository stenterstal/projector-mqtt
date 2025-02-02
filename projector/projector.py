import subprocess
from enum import Enum


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
                print("[Projector] Turned on")
                return True
            print("[Projector] Something went wrong trying to turn on projector")
        return False

    def turn_off(self) -> bool:
        if self.state == ProjectorState.running:
            process = subprocess.Popen("echo 0 > /sys/class/gpio/gpio48/value", stdout=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if not error:
                self.state = ProjectorState('stopped')
                print("[Projector] Turned off")
                return True
            print("[Projector] Something went wrong trying to turn off projector")
        return False

    def __getstate__(self) -> ProjectorState:
        return self.state