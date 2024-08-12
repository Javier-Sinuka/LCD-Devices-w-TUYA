from local.tuya.tuya_handler import TuyaHandler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

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
            print(f"Error inr __run_devices: {e}")

    def start(self, sampling_time_in_minutes: int):
        self.__scheduler.add_job(self.run_devices, 'interval', minutes=sampling_time_in_minutes)
        self.__scheduler.start()
        print("Starting device sampling.")
        self.run_devices()

    def stop(self):
        self.__scheduler.shutdown(wait=False)
        print("Stopping device sampling.")