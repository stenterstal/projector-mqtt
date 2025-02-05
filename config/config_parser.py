import io
import os
from configparser import ConfigParser


def write_config(section: str, data: dict):
    from app import ROOT_DIR
    config = ConfigParser(defaults=None)

    config.read(os.path.join(ROOT_DIR, 'config.ini'))

    config[section] = data

    config.write(io.open(os.path.join(ROOT_DIR, 'config.ini'), 'w'))


def read_config():
    from app import ROOT_DIR
    config = ConfigParser(defaults=None)
    config.read(os.path.join(ROOT_DIR, 'config.ini'))

    # Return the config as list
    return {s:dict(config.items(s)) for s in config.sections()}

def validate_config():
    from app import ROOT_DIR
    config = ConfigParser(defaults=None)
    config.read(os.path.join(ROOT_DIR, 'config.ini'))

    required_sections = {
        'config': ['valid'],
        'mqtt': ['address', 'port', 'user', 'password'],
        'homeassistant': ['id', 'command_topic', 'state_topic']
    }

    errors = []

    # Check if required sections exist
    for section, required_fields in required_sections.items():
        if not config.has_section(section):
            errors.append(f"Missing section: {section}")
            continue  # Skip further checks for this section if it's missing

        # Check if required fields exist within the section
        for field in required_fields:
            if not config.has_option(section, field):
                errors.append(f"Missing field '{field}' in section '{section}'")

    return errors