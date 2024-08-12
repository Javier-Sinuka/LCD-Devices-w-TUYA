import os
import time
from datetime import datetime, timedelta, timezone
import json
import tinytuya
# import tuyapower
# tinytuya.set_debug(True)

class LocalModelTuya:
    __devices_acces = {}
    __devices_mapping = {}
    file_name = ''
    mapping_file_name = ''

    def __init__(self, file_name='local_data_devices/acces_tuya.json',
                 mapping_file_name='local_data_devices/mapping_tuya.json'):
        self.file_name = file_name
        self.mapping_file_name = mapping_file_name
        self.__devices_acces = {}
        self.__devices_mapping = {}
        self.safe_to_json()

    def safe_to_json(self):
        """
            Metodo para almacenar las credenciales de los dispositivos presentes en la red local
            en un archivo JSON.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        acces_path = os.path.join(current_dir, self.file_name)
        mapping_path = os.path.join(current_dir, self.mapping_file_name)
        data = self.get_file_info("../../devices.json")

        for element in data:
            if 'id' in element and 'ip' in element and 'key' in element and 'mapping' in element:
                self.__devices_acces[element['name']] = {
                    'id': element['id'],
                    'ip': element['ip'],
                    'key': element['key'],
                    'version': element['version']
                }
                self.__devices_mapping[element['id']] = {
                    'mapping': element['mapping']
                }
            else:
                print(f"Elemento inválido encontrado y omitido: {element}")

        with open(acces_path, 'w') as json_file:
            json.dump(self.__devices_acces, json_file, indent=4)
        with open(mapping_path, 'w') as json_file:
            json.dump(self.__devices_mapping, json_file, indent=4)

    def get_file_info(self, direction_file):
        """
            Metodo que devuelve el contenido de un archivo especificado por su direccin relativa.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, f"{direction_file}")
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            return data

        except FileNotFoundError:
            print("No such 'devices.json'.")
            return
        except json.JSONDecodeError:
            print("Error to decodificate JSON format.")
            return

    def get_all_acces_data(self):
        """
            Metodo que devuelve la informacion de acceso local de todos los dispositivos.
        """
        return self.get_file_info('local_data_devices/acces_tuya.json')

    def get_all_mapping_data(self):
        """
            Metodo que devuelve la informacion de mappeo de los codigos de modificacion/lectura
            de los dispositivos TUYA.
        """
        return self.get_file_info('local_data_devices/mapping_tuya.json')

    def get_code_mapping(self, device_id: str):
        mapping = self.get_all_mapping_data().get(device_id).get('mapping')
        data = []
        for element in mapping:
            data.append(element)
        return data

    def get_name_code_mapping(self, device_id: str, code: str):
        mapping = self.get_all_mapping_data().get(device_id).get('mapping')
        name = mapping.get(code).get('code')
        return name

    def get_device_acces_data(self, device_id):
        """
            Metodo que devuelve el la informacion de acceso de un dispositivo especifico, solicitado
            por su ID.
        """
        data = {}
        for acces in self.__devices_acces.values():
            if acces['id'] == device_id:
                data = acces
        return data

    def get_device_individual_info(self, device_id):
        """
            Devuelve una lista con la TODA la informacion asociada a un dispositivo especifico,
            ingresando unicamente su id.

            :param device_id:
            :return:
        """
        data = self.get_file_info("../../devices.json")
        dev_list = []
        for element in data:
            if element['id'] == device_id:
                dev_list.append(element)
        return dev_list

class LocalConnection(LocalModelTuya):
    def __init__(self):
        super().__init__()

    def get_status_device_tuya(self, device_id: str):
        """
        Metodo que devuelve los valores medidos por un dispositivo que se encuentra activo en la red local.

        Parameters:
        device_id (str): The ID of the device.

        Returns:
        List[dps]: The value of the device local.
        """
        cred = LocalModelTuya().get_device_acces_data(device_id)
        # print(cred)
        dev = tinytuya.OutletDevice(cred['id'],
                                    cred['ip'],
                                    cred['key'])
        dev.set_version(float(cred['version']))
        data = {}
        try:
            data = dev.status()
        except KeyboardInterrupt:
            print(
                "CANCEL: Interruption for keyboard %s [%s]."
                % (cred['id'], cred['ip'])
            )
        except Exception as e:
            print(f"An error occurred while obtaining device status: {e}")

        try:
            dps = data['dps']
            if dps:
                return dps
            else:
                print("DPS Empty")
                return
        except Exception as e:
            print(f"An error occurred whilef trying to read the device information: {e}")