import os
import threading

from config.config_listener import ConfigListener
from dashboard.flask import app
from projector.projector import Projector

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Runs the flask interface
def run_flask():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)

# Runs the MQTT broker and turns on/off the projector on message
def run_projector_mqtt():
    Projector()

# Reloads the front-end when the config is changed
def run_config_listener():
    ConfigListener(ROOT_DIR)

if __name__ == '__main__':
    # Create threads for Flask and normal app
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    projector_thread = threading.Thread(target=run_projector_mqtt, daemon=True)
    config_thread = threading.Thread(target=run_config_listener, daemon=True)

    # Start both threads
    flask_thread.start()
    projector_thread.start()
    config_thread.start()

    # Wait for both threads to finish
    flask_thread.join()
    projector_thread.join()
    config_thread.join()