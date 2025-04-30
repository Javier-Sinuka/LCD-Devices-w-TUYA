import json
import time

import tinytuya
from pathlib import Path

class LocalModelTuya:
    __devices_acces = {}
    __devices_mapping = {}
    file_name = ''
    mapping_file_name = ''

    def __init__(self, file_name='local_data_devices/acces_tuya.json',
                 mapping_file_name='local_data_devices/mapping_tuya.json'):
        current_dir = Path(__file__).resolve().parent
        self.file_name = current_dir / file_name
        self.mapping_file_name = current_dir / mapping_file_name

        self.__devices_acces = {}
        self.__devices_mapping = {}

    def safe_to_json(self):
        """
            Metodo para almacenar las credenciales de los dispositivos presentes en la red local
            en un archivo JSON.
        """
        try:
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
                    print(f"Invalid element found and skipped: {element}")

            with open(self.file_name, 'w') as json_file:
                json.dump(self.__devices_acces, json_file, indent=4)
            with open(self.mapping_file_name, 'w') as json_file:
                json.dump(self.__devices_mapping, json_file, indent=4)
        except Exception as e:
            raise e

    def update_devices_ip(self):
        """
           Metodo para actualizar las IP de los dispositivos almacenados, teniendo en cuenta
           que los valores nuevos son tomados del archivo 'snapshot.json' generado por el metodo
           scan de Tinytuya.
        """
        snapshot_data = self.get_file_info("../../snapshot.json")
        devices_data = self.get_file_info(self.file_name)

        flag = True
        counter = 0
        for device in snapshot_data["devices"]:
            device_name = device["name"]
            device_ip = device["ip"]

            if device_name in devices_data:
                stored_device = devices_data[device_name]
                if stored_device["ip"] != device_ip:
                    devices_data[device_name]["ip"] = device_ip
                    flag = False
                    counter+=1

        with open(self.file_name, 'w') as f:
            json.dump(devices_data, f, indent=4)
            if flag:
                print("There are no modified ips.")
            else:
                print(f"There a {counter} IPs updates successful.")

    def get_file_info(self, direction_file):
        """
            Metodo que devuelve el contenido de un archivo especificado por su direccion relativa.
        """
        current_dir = Path(__file__).resolve().parent
        json_path = current_dir / direction_file

        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            return data

        except FileNotFoundError:
            print(f"No such file: '{json_path}'.")
            return
        except json.JSONDecodeError:
            print("Error decoding JSON format.")
            return

    def get_all_acces_data(self):
        """
            Metodo que devuelve la informacion de acceso local de todos los dispositivos.
        """
        return self.get_file_info(self.file_name)

    def get_all_mapping_data(self):
        """
            Metodo que devuelve la informacion de mappeo de los codigos de modificacion/lectura
            de los dispositivos TUYA.
        """
        return self.get_file_info(self.mapping_file_name)

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
        file_data = self.get_file_info(self.file_name)
        if not file_data:
            return None

        for device_name, device_info in file_data.items():
            if device_info.get("id") == device_id:
                return device_info

        print(f"Device with ID '{device_id}' not found.")
        return None

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
        # tinytuya.set_debug(True)
        dev = tinytuya.OutletDevice(cred['id'],
                                    cred['ip'],
                                    cred['key'])
        dev.set_version(float(cred['version']))
        data = {}
        time.sleep(5)
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
            print(data)