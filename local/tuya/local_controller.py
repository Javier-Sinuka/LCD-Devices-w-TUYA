from datetime import datetime
import time, requests, json
from sqlite3 import IntegrityError

from local_model import LocalConnection

BASE_URL = "http://127.0.0.1:8001"

class LocalController():
    __local_connection = LocalConnection
    def __init__(self):
        self.initialized = False
        self.__local_connection = LocalConnection()
        if not self.initialized:
            self.save_devices_info()
            self.save_attributes_local_device()
            self.initialized = True

    def post_element(self, url: str, payload: json):
        response = requests.post(url, json=payload)
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.json()

    def get_element(self, url: str):
        response = requests.get(url)
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.json()

    def get_device_id(self, unique_device_id: str):
        try:
            url = f"{BASE_URL}/devices/get_id/{unique_device_id}"
            return self.get_element(url)['id']
        except Exception as e:
            print(f"Error in get_device_id: {e}")

    def get_attribute_id(self, name: str):
        try:
            url = f"{BASE_URL}/attributes/get_attribute/{name}"
            return self.get_element(url)['id']
        except Exception as e:
            print(f"Error in get_attribute_id: {e}")

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
            try:
                self.post_element(url, payload)
            except Exception as e:
                if "Unique constraint violated." in str(e):
                    pass
                else:
                    print(f"Error save_attribute_local_device: {e}")

    def save_attributes_local_device(self):
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
                try:
                    self.post_element(url, payload)
                except Exception as e:
                    if "Unique constraint violated." in str(e):
                        pass
                    else:
                        print(f"Error save_attribute_local_device: {e}")

    def save_content_devices(self):
        url = f"{BASE_URL}/values/create"
        devices_acces_data = self.__local_connection.get_all_acces_data()

        for device_data in devices_acces_data:
            device_id = devices_acces_data[device_data].get('id')

            value_device = self.__local_connection.get_status_device_tuya(device_id=device_id)

            pk_device = self.get_device_id(device_id)

            local_code_device = self.__local_connection.get_code_mapping(device_id)

            for value in value_device:
                if value in local_code_device:
                    name_value = self.__local_connection.get_name_code_mapping(device_id=device_id, code=value)
                    pk_attribute = self.get_attribute_id(name_value)

                    payload = {
                        'value': str(value_device[value]),
                        'device_id': pk_device,
                        'attribute_id': pk_attribute,
                    }

                    try:
                        self.post_element(url, payload)
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error save_content_device: {e}")


d = LocalController()
for i in range(0, 5):
    d.save_content_devices()
# d.save_attributes_local_devicec()







