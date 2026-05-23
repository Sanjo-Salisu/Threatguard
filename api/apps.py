from django.apps import AppConfig
import threading
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):

        if os.environ.get('RUN_MAIN') == 'true':

            from .usb_monitor import start_usb_monitor
            from .file_monitor import start_file_monitor

            threading.Thread(target=start_usb_monitor, daemon=True).start()
            threading.Thread(target=start_file_monitor, daemon=True).start()

            print("USB + FILE MONITORS STARTED")