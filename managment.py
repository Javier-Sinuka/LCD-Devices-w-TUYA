from local.tuya.tuya_handler import TuyaHandler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging, subprocess, time

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class Manager():
    __tuya_handler = TuyaHandler

    def __init__(self):
        self.devices = []
        self.__tuya_handler = TuyaHandler()
        self.__scheduler = BlockingScheduler()

        self.devices.append(self.__tuya_handler)

    def run_devices(self):
        try:
            for device in self.devices:
                device.save_content_devices()
        except Exception as e:
            print(f"Error in __run_devices: {e}")

    def start(self, sampling_time_in_minutes: int):
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.add_job(self.run_command_with_confirmation, "interval", minutes=60)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

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