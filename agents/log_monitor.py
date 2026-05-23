import win32evtlog
import requests
import socket
import time

SERVER_URL = "http://127.0.0.1:8000/api/event/"
SERVER = "localhost"
LOG_TYPE = "Security"


def send_event(description, severity="MEDIUM"):

    data = {
        "hostname": socket.gethostname(),
        "ip_address": "127.0.0.1",
        "event_type": "LOGIN-AUDIT",
        "severity": severity,
        "description": description
    }

    try:
        requests.post(SERVER_URL, json=data, timeout=5)
        print("SENT:", description)
    except Exception as e:
        print("ERROR:", e)


def run_log_agent():

    print("LOG AGENT STARTED")

    hand = win32evtlog.OpenEventLog(SERVER, LOG_TYPE)

    flags = (
        win32evtlog.EVENTLOG_BACKWARDS_READ |
        win32evtlog.EVENTLOG_SEQUENTIAL_READ
    )

    seen = set()
    failed = 0

    while True:

        events = win32evtlog.ReadEventLog(hand, flags, 0)

        if events:

            for e in events:

                if e.RecordNumber in seen:
                    continue

                seen.add(e.RecordNumber)

                eid = int(e.EventID) & 0xFFFF

                # FAILED LOGIN
                if eid == 4625:
                    failed += 1
                    send_event("Failed login attempt detected", "HIGH")

                # SUCCESS LOGIN
                elif eid == 4624:

                    if failed > 0:
                        send_event(
                            f"{failed} failed login(s) before success",
                            "HIGH"
                        )
                    else:
                        send_event("Successful login detected", "LOW")

                    failed = 0

        time.sleep(1)


if __name__ == "__main__":
    run_log_agent()