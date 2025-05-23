from connectors.dashboard import DashboardManager
from local.tuya.local_model import LocalModelTuya
from local.tuya.tuya_handler import TuyaHandler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging, subprocess, time
from datetime import datetime, timedelta
from connectors.backup.backup_database import GoogleDriveConnector
import os
import re

def get_actual_local_path(file_name):
    actual_directory = os.path.dirname(os.path.abspath(__file__))
    complet_path = os.path.join(actual_directory, file_name)
    return complet_path

# Basic Configuration for the log in file
file_path = get_actual_local_path('logs')
current_time = datetime.now().strftime("%Y_%m_%d_%H%M")
log_filename = f"{file_path}/record_library_{current_time}.txt"
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[    # Establecer la variable de entorno COMPOSE_FILE si se usa un archivo distinto al por defecto

        logging.FileHandler(log_filename),
    ])
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class Manager(DashboardManager):
    __tuya_handler = TuyaHandler
    __tuya_model = LocalModelTuya

    def __init__(self):
        super().__init__()
        self.devices = []
        self.__tuya_handler = TuyaHandler()
        self.__tuya_model = LocalModelTuya()
        self.__scheduler = BlockingScheduler()
        self.devices.append(self.__tuya_handler)

    def start(self, sampling_time_in_minutes: int):
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=120)
        self.__scheduler.add_job(self.update_devices_ip, "interval", minutes=122)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=120)
        self.__scheduler.add_job(self.update_devices_ip, "interval", minutes=122)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_dashboard(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send_automatization(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=120)
        self.__scheduler.add_job(self.update_devices_ip, "interval", minutes=122)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_dashboard(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send_with_backup(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int, file_path: str, folder_id: str):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=120)
        self.__scheduler.add_job(self.update_devices_ip, "interval", minutes=122)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_dashboard(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.add_job(lambda: self.update_backup_database(file_path, folder_id), 'interval', minutes=60)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send_with_backup_automatization(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int, file_path: str, folder_id: str):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=120)
        self.__scheduler.add_job(self.update_devices_ip, "interval", minutes=122)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_dashboard(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.add_job(lambda: self.update_backup_database(file_path, folder_id), 'interval', minutes=60)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def run_command_update_scan(self):
        try:
            command = ['python3', '-m', 'tinytuya', 'scan']
            subprocess.run(command, check=True)
            print("Scan executed successfully.")
            print("\nUpdate content.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error with executed command 'python -m tinituya scan': {e}")

    def stop(self):
        self.__scheduler.shutdown(wait=False)
        print("Stopping device sampling.")

    def update_devices_ip(self):
        self.__tuya_model.safe_to_json()

    def run_devices(self):
        try:
            for device in self.devices:
                device.save_content_devices()
        except Exception as e:
            print(f"Error in __run_devices: {e}")

    def update_backup_database(self, name_file_databes: str, folder_id: str):
        actual_day = datetime.now().day
        actual_hour = datetime.now().hour
        if (actual_day % 7 == 0 or actual_day == 1) and (actual_hour % 13 == 0 or actual_hour % 23 == 0):
            path_database = get_actual_local_path(name_file_databes)
            backup = GoogleDriveConnector(path_database, folder_id)
            backup.update_backup()