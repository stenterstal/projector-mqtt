from enum import Enum


class MqttState(str, Enum):
    stopped = 'stopped'     # MQTT is not running
    running = 'running'     # MQTT is running
    failed = 'failed'       # Something went wrong while connecting

    def __str__(self) -> str:
        return self.value