from datetime import datetime
from enum import Enum


# Colors
grey = "\x1b[38;20m"
light_green = "\033[1;32m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

class LogPrefix(str, Enum):
    projector = 'PROJ'
    dashboard = 'DASH'
    mqtt = 'MQTT'
    conf = 'CONF'

class Logger:
    def __init__(self, prefix: LogPrefix):
        self.prefix = prefix

    def info(self, message: str):
        log_date = datetime.now().strftime("%H:%M:%S")
        print(light_green + "[" + log_date + "] [" + self.prefix + "] " + message + reset)

    def warn(self, message: str):
        log_date = datetime.now().strftime("%H:%M:%S")
        print(yellow + "[" + log_date + "] ["+ self.prefix + "] " + message + reset)

    def error(self, message: str):
        log_date = datetime.now().strftime("%H:%M:%S")
        print(red + "[" + log_date + "] [" + self.prefix + "] " + message + reset)