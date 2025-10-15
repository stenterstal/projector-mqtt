import os
import subprocess
import time
import threading

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config.config_parser import validate_config
from log import Logger, LogPrefix
from projector.projector import Projector

# from app import ROOT_DIR

class ConfigListener:
    def __init__(self, root_dir):
        self.path = os.path.join(root_dir)
        self.conf_log = Logger(LogPrefix.conf)

        observer = Observer()
        # Listen to the root dir, config.ini might not exist yet
        observer.schedule(ConfigFileChangedHandler(root_dir), self.path, recursive=False)
        observer.start()
        try:
            self.conf_log.info(f"Watching for changes...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class ConfigFileChangedHandler(FileSystemEventHandler):
    def __init__(self, root_dir):
        self.conf_log = Logger(LogPrefix.conf)
        self.root_dir = root_dir

    def on_modified(self, event) -> None:
        # Don't listen on directory
        if event.is_directory:
            return
        
        print(event)

        if event.src_path == os.path.join(self.root_dir, 'config.ini'):
            self.conf_log.info('config.ini was edited')

            config_errors = validate_config()
            if len(config_errors) == 0:
                self.conf_log.info('config.ini has all required fields, reloading display...')
                subprocess.run(["/usr/bin/sudo", "xdotool", "key", "ctrl+r"])
            else:
                self.conf_log.error("Found {} errors in config".format(len(config_errors)))
                for error in config_errors:
                    self.conf_log.error(error)