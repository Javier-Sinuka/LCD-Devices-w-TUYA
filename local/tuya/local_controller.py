from datetime import datetime
import time, requests, json
from local_model import LocalConnection

BASE_URL = "http://127.0.0.1:8009"

class LocalController():
    __local_connection = LocalConnection
    def __init__(self):
        self.__local_connection = LocalConnection()
        self.save_devices_info()

    def save_devices_info(self):
        url = f"{BASE_URL}/devices/create"
        devices_acces_data = self.__local_connection.get_all_acces_data()
        for device_data in devices_acces_data:
            device_id = devices_acces_data[device_data].get('id')
            payload = {
                "name": device_data,
                "unique_device_id": device_id,
                "manufacturer": 'TUYA',
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Device {payload['name']} created successfully")
            else:
                print(f"Device {payload['name']} failed to create")
            time.sleep(0.1)


d = LocalController()
d.save_devices_info()







