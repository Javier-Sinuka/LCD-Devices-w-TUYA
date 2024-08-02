from datetime import datetime
import time, requests, json
from local_model import LocalConnection

BASE_URL = "http://127.0.0.1:8001"

class LocalController():
    __local_connection = LocalConnection
    def __init__(self):
        self.__local_connection = LocalConnection()
        self.save_devices_info()
        self.save_attributes_local_devicec()

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
                pass
            else:
                print(f"Device {payload['name']} failed to create")
            time.sleep(0.01)

    def save_attributes_local_devicec(self):
        url = f"{BASE_URL}/attributes/create"
        attributes_acces_data = self.__local_connection.get_all_mapping_data()
        for attribute_data in attributes_acces_data:
            attr = attributes_acces_data[attribute_data]['mapping']
            for attribute in attr:
                unit = ''
                try:
                    if attr[attribute]['values']['unit']:
                        unit = attr[attribute]['values']['unit']
                except:
                    unit = 'none'
                payload = {
                    'name': attr[attribute]['code'],
                    'unit': unit,
                    'data_type': attr[attribute]['type'],
                }
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    pass
                else:
                    print(f"Attribute {payload['name']} failed to create")
                time.sleep(0.01)

    def read_content_devices(self):
        url = f"{BASE_URL}/values/create"
        devices_acces_data = self.__local_connection.get_all_acces_data()

        for device_data in devices_acces_data:
            device_id = devices_acces_data[device_data].get('id')
            print(device_id)

            value_device = self.__local_connection.get_status_device_tuya(device_id=device_id)

            print(value_device)

            pk_device = self.get_device_id(device_id)

            local_code_device = self.__local_connection.get_code_mapping(device_id)

            for value in value_device:
                if value in local_code_device:
                    name_value = self.__local_connection.get_name_code_mapping(device_id=device_id,code=value)
                    pk_attribute = self.get_attribute_id(name_value)

                    payload = {
                        'device_id': pk_device,
                        'attribute_id': pk_attribute,
                        'value': value_device[value],
                        'timestamp': datetime.now().isoformat(),
                    }

                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        return response
                    else:
                        print(f"Value failed to write")
                    time.sleep(0.01)

    def get_device_id(self, unique_device_id: str):
        url = f"{BASE_URL}/devices/get_id/{unique_device_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['id']
        else:
            print(f"Device {unique_device_id} failed to read")
        time.sleep(0.01)

    def get_attribute_id(self, name: str):
        url = f"{BASE_URL}/attributes/get_attribute/{name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['id']
        else:
            print(f"Device {name} failed to read")
        time.sleep(0.01)

d = LocalController()
d.read_content_devices()
# d.save_attributes_local_devicec()







