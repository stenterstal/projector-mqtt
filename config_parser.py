import io
from configparser import SafeConfigParser


def write_config(data: dict):
    ini = SafeConfigParser(defaults=None)

    sections = data.keys()
    ini.add_section('config')
    for section in sections:
        ini.set('config', section, data[section] or ' ')

    ini.write(io.open('config.ini', 'w'))


def read_config():
    ini = SafeConfigParser(defaults=None)
    ini.read('config.ini')

    if not ini.has_section('config'):
        return dict()

    data = dict()
    for key in ini['config']:
        data[key] = ini['config'][key]
    return data