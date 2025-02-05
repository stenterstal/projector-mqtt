import os
import threading

from dashboard.flask import app
from projector.dynamic_projector import DynamicProjectorLoop

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_flask():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)

def run_projector_mqtt():
    DynamicProjectorLoop()

if __name__ == '__main__':
    # Create threads for Flask and normal app
    flask_thread = threading.Thread(target=run_flask)
    projector_thread = threading.Thread(target=run_projector_mqtt)

    # Start both threads
    flask_thread.start()
    projector_thread.start()

    # Wait for both threads to finish
    flask_thread.join()
    projector_thread.join()
