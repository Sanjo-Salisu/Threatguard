from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import requests
import socket
import time


SERVER_URL = "http://127.0.0.1:8000/api/event/"


class ThreatHandler(FileSystemEventHandler):

    def send_event(self, description):

        hostname = socket.gethostname()

        data = {
            "hostname": hostname,
            "ip_address": "127.0.0.1",
            "event_type": "FILE",
            "severity": "HIGH",
            "description": description
        }

        try:
            requests.post(SERVER_URL, json=data)
            print("Event Sent:", description)

        except Exception as e:
            print("Error:", e)

    def on_modified(self, event):

        if not event.is_directory:

            description = f"File Modified: {event.src_path}"

            self.send_event(description)

    def on_created(self, event):

        if not event.is_directory:

            description = f"File Created: {event.src_path}"

            self.send_event(description)

    def on_deleted(self, event):

        if not event.is_directory:

            description = f"File Deleted: {event.src_path}"

            self.send_event(description)


def start_file_monitor():

    path_to_watch = "C:/Users/iCreabot/Desktop/test_folder"

    event_handler = ThreatHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        path=path_to_watch,
        recursive=True
    )

    observer.start()

    print("File Monitoring started...")

    try:

        while True:
            time.sleep(1)

    except Exception as e:

        print("Monitor Error:", e)

        observer.stop()

    observer.join()