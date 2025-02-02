import threading
import time

import flask

from dashboard.flask import app
from mqtt.mqtt import Mqtt


def run_flask():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)

def run_mqtt():
    Mqtt()

if __name__ == '__main__':
    # Create threads for Flask and normal app
    flask_thread = threading.Thread(target=run_flask)
    normal_thread = threading.Thread(target=run_mqtt)

    # Start both threads
    flask_thread.start()
    normal_thread.start()

    # Wait for both threads to finish
    flask_thread.join()
    normal_thread.join()
