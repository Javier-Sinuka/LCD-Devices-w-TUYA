from datetime import datetime
import time, requests, json
from local_model import LocalConnection

BASE_URL = "http://127.0.0.1:8001"

class LocalController():
    __local_connection = LocalConnection
    def __init__(self):
        self.save_devices_info()
        self.__local_connection = LocalConnection()

    def save_devices_info(self):
        devices_acces_data = self.__local_connection.get_all_acces_data()
        for device_data in devices_acces_data:
            device_id = devices_acces_data[device_data].get('id')

            try:
                for j in data_local:
                    id_dev = self.db.query(Devices).filter_by(device_id=device_id).first().id
                    try:  # Existe un valor que no lo registra el dispositivo de medidor de aire
                        id_attr = self.db.query(Attributes).filter_by(ref_attr_device=j).first().id
                    except Exception:
                        id_attr = 'unregistered_attribute'
                    value = Values(device_id=id_dev,
                                   attribute_id=id_attr,
                                   value=data_local[j],
                                   timestamp=datetime.now())
                    self.put_data(self.db, value)
            except Exception:
                print("Elemento no iterable")
            time.sleep(2)

    def save_device_data(self):
        acces_data = self.__local_model.get_all_acces_data()
        # mapping_data = self.__local_model.get_all_mapping_data()
        for element in acces_data:
            existing_device_name = self.db.query(Devices).filter(Devices.name == element).first()
            existing_device_id = self.db.query(Devices).filter(Devices.unique_device_id == acces_data[element]['id']).first()
            if not existing_device_name and not existing_device_id:
                data_device = Devices(name=element, unique_device_id=acces_data[element]['id'], manufacturer="TUYA")

                # mapping = mapping_data[acces_data[element]['id']]['mapping']
                # self.save_attributes(mapping)

                self.put_data(self.db, data_device)

    def save_attributes(self, mapping: dict):
        for data in mapping:
            existing_attribute_ref = self.db.query(Attributes).filter(Attributes.ref_attr_device == data).first()
            if not existing_attribute_ref:
                unit = ''
                try:
                    unit = mapping[data]['values']['unit']
                except Exception:
                    unit = 'none'
                data_attribute = Attributes(ref_attr_device=data,
                                            name=mapping[data]['code'],
                                            unit=unit,
                                            data_type=mapping[data]['type'])
                self.put_data(self.db, data_attribute)








