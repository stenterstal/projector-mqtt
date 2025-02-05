import os
import time

from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from watchdog.observers import Observer

from config.config_parser import validate_config
from log import Logger, LogPrefix
from projector.projector import Projector


class DynamicProjectorStarter(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0
        self.debounce_time = 0.5
        self.conf_log = Logger(LogPrefix.conf)
        self.projector = Projector()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        # Don't listen on directory
        if event.is_directory:
            return

        # Ignore if the event occurred too soon after the last one
        current_time = time.time()
        if current_time - self.last_modified < self.debounce_time:
            return

        from app import ROOT_DIR

        if event.src_path == os.path.join(ROOT_DIR, 'config.ini'):
            self.last_modified = current_time
            self.conf_log.info('config.ini was edited')

            config_errors = validate_config()
            if len(config_errors) == 0:
                self.conf_log.info('config.ini has all required fields, starting projector...')
                # Only start projector if all fields are present
                self.projector = Projector()


def DynamicProjectorLoop():
    from app import ROOT_DIR
    event_handler = DynamicProjectorStarter()
    observer = Observer()
    # Listen to the root dir, config.ini might not exist yet
    observer.schedule(event_handler, os.path.join(ROOT_DIR), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()