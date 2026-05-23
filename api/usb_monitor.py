import psutil
import time
import requests
import socket

SERVER_URL = "http://127.0.0.1:8000/api/event/"

known_drives = set()


def send_event(drive):
    hostname = socket.gethostname()

    data = {
        "hostname": hostname,
        "ip_address": "127.0.0.1",
        "event_type": "USB",
        "severity": "HIGH",
        "description": f"USB Drive Detected: {drive}"
    }

    try:
        requests.post(SERVER_URL, json=data)
        print("USB EVENT SENT:", drive)
    except Exception as e:
        print("Error:", e)


def start_usb_monitor():
    global known_drives

    print("Monitoring USB drives...")

    while True:
        current_drives = set()

        for part in psutil.disk_partitions():
            if "removable" in part.opts.lower():
                current_drives.add(part.device)

        new_drives = current_drives - known_drives

        for drive in new_drives:
            send_event(drive)

        known_drives = current_drives

        time.sleep(2)