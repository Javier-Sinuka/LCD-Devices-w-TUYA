from connectors.dashboard import DashboardManager
from local.tuya.tuya_handler import TuyaHandler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging, subprocess, time
from datetime import datetime, timedelta
from connectors.backup.backup_database import GoogleDriveConnector
import os

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
    handlers=[
        logging.FileHandler(log_filename),
    ])
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class Manager(DashboardManager):
    __tuya_handler = TuyaHandler

    def __init__(self):
        super().__init__()
        self.devices = []
        self.__tuya_handler = TuyaHandler()
        self.__scheduler = BlockingScheduler()
        self.devices.append(self.__tuya_handler)

    def start(self, sampling_time_in_minutes: int):
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_with_confirmation, "interval", minutes=60)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_with_confirmation, "interval", minutes=60)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_tago(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send_automatization(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=60)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_tago(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send_with_backup(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int, file_path: str, folder_id: str):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=60)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_tago(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.add_job(lambda: self.update_backup_database(file_path, folder_id), 'interval', minutes=60)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def start_and_send_with_backup_automatization(self, sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int, file_path: str, folder_id: str):
        current_time = datetime.now()
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_update_scan, "interval", minutes=60)
        start_time_for_tago = current_time + timedelta(minutes=sampling_time_in_minutes+5)
        self.__scheduler.add_job(lambda: self.send_to_tago(token, time_to_send_dashboard), 'interval', minutes=time_to_send_dashboard, start_date=start_time_for_tago)
        self.__scheduler.add_job(lambda: self.update_backup_database(file_path, folder_id), 'interval', minutes=60)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def run_command_update_scan(self):
        try:
            command = ['python3', '-m', 'tinytuya', 'scan']
            subprocess.run(command, check=True)
            print("Scan executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error with executed command 'python -m tinituya scan': {e}")

    def stop(self):
        self.__scheduler.shutdown(wait=False)
        print("Stopping device sampling.")

    def run_command_with_confirmation(self, command="python -m tinytuya wizard", confirmations= None, delay=10):
        if confirmations is None:
            confirmations = ['Y','Y','Y']
        try:
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)

            for confirmation in confirmations:
                process.stdin.write(confirmation + '\n')
                process.stdin.flush()
                time.sleep(delay)

            stdout, stderr = process.communicate()

            print(stdout)

            if stderr:
                print(f"Error: {stderr}")

        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")

    def run_devices(self):
        try:
            for device in self.devices:
                device.save_content_devices()
        except Exception as e:
            print(f"Error in __run_devices: {e}")

    def update_backup_database(self, name_file_databes: str, folder_id: str):
        actual_day = datetime.now().day
        actual_hour = datetime.now().hour
        if actual_day % 7 == 0 and (actual_hour % 12 == 0 or actual_hour % 23 == 0):
            path_database = get_actual_local_path(name_file_databes)
            backup = GoogleDriveConnector(path_database, folder_id)
            backup.update_backup()