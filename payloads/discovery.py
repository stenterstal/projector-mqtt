def make_discovery_message(mqtt_id):
  return {
    "device": {
      "name": "Alarm Projector",
      "ids": mqtt_id,
      "manufacturer": "Texas Instruments / Beaglebone",
      "model": "DLPDLCR2000EVM"
    },
    "origin": {
      "name": "Sten ter Stal"
    },
    "components": {
      "projector": {
        "platform": "switch",
        "unique_id": mqtt_id,
        "name": "Projector",
        "icon": "mdi:projector"
      }
    },
    "command_topic": "homeassistant/switch/"+mqtt_id+"/set"
  }