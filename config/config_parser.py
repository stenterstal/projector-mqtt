import io
import os
from configparser import ConfigParser


def write_config(section: str,data: dict):
    from app import ROOT_DIR
    config = ConfigParser(defaults=None)

    config.read(os.path.join(ROOT_DIR, 'config.ini'))

    sections = data.keys().mapping

    config[section] = sections

    config.write(io.open(os.path.join(ROOT_DIR, 'config.ini'), 'w'))


def read_config():
    from app import ROOT_DIR
    config = ConfigParser(defaults=None)
    config.read(os.path.join(ROOT_DIR, 'config.ini'))

    # Return the config as list
    return {s:dict(config.items(s)) for s in config.sections()}