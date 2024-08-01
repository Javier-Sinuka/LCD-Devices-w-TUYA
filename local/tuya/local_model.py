import os
import time
from datetime import datetime, timedelta, timezone
import json
import tinytuya
# import tuyapower
import numpy
# tinytuya.set_debug(True)

class LocalModelTuya:
    __devices_acces = {}
    __devices_data = {}
    __mapping_data = {}
    file_name = ''
    mapping_file_name = ''

    def __init__(self, file_name='local_data_devices/acces_tuya.json',
                 mapping_file_name='local_data_devices/mapping_tuya.json'):
        self.file_name = file_name
        self.mapping_file_name = mapping_file_name
        self.__devices_data = {}
        self.__devices_acces = {}
        self.__mapping_data = {}
        self.safe_to_json()

    """
        Metodo para almacenar las credenciales de los dispositivos presentes en la red local
        en un archivo JSON.
    """
    def safe_to_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        acces_path = os.path.join(current_dir, self.file_name)
        mapping_path = os.path.join(current_dir, self.mapping_file_name)
        data = self.get_device_info()

        for element in data:
            if 'id' in element and 'ip' in element and 'key' in element and 'mapping' in element:
                self.__devices_acces[element['name']] = {
                    'id': element['id'],
                    'ip': element['ip'],
                    'key': element['key'],
                    'version': element['version']
                }
                self.__mapping_data[element['id']] = {
                    'mapping': element['mapping']
                }
            else:
                print(f"Elemento inválido encontrado y omitido: {element}")

        with open(acces_path, 'w') as json_file:
            json.dump(self.__devices_acces, json_file, indent=4)
        with open(mapping_path, 'w') as json_file:
            json.dump(self.__mapping_data, json_file, indent=4)

    """
        Representacion en formato ano-mes-dia-hora-minuto-segundo-milisegundo de un valor en milisegundos
    """
    def conversor_time_hours(self, time_r: int, format='YY:MM:DD'):
        utc_date = datetime.fromtimestamp((time_r / 1000.0), tz=timezone.utc)
        utc_hour = timezone(timedelta(hours=-3))
        utc_time = utc_date.astimezone(utc_hour)
        date = ''
        if format == 'HH':
            date = utc_time.strftime('%H')
        elif format == 'YY:MM:DD':
            date = utc_time.strftime('%Y-%m-%d-%h-%m-%s-%ms')
        return date

    """
        Metodo que devuelve el tiempo actual en milisegundos.
    """
    def get_actual_time(self):
        return int(time.time() * 1000)

    """
        Metodo que devuelve la informacion de acceso local de todos los dispositivos.
    """
    def get_all_acces_data(self):
        try:
            with open('local_data_devices/acces_tuya.json', 'r') as file:
                data = json.load(file)
            return data
        except Exception:
            print("Error al abrir archivo con todos los datos de acceso.")
            return

    def get_all_mapping_data(self):
        try:
            with open('local_data_devices/mapping_tuya.json', 'r') as file:
                data = json.load(file)
            return data
        except Exception:
            print("Error al abrir archivo con todos los datos de mapeo.")
            return

    """
        Metodo que devuelve el la informacion de acceso de un dispositivo especifico, solicitado
        por su ID.
    """
    def get_device_acces_data(self, device_id):
        data = {}
        for acces in self.__devices_acces.values():
            if acces['id'] == device_id:
                data = acces
        return data

    """
        Devuelve una lista con la TODA la informacion asociada a un dispositivo especifico, 
        ingresando unicamente su id.
    """
    def get_device_individual_info(self, device_id):
        data = self.get_device_info()
        dev_list = []
        for element in data:
            if element['id'] == device_id:
                dev_list.append(element)
        return dev_list
    """
        Metodo que devuelve la informacion local de los dispositvos, generada por la libreria
        TINYTUYA.
    """
    def get_device_info(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '../../devices.json')
        data = {}
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
                self.__devices_data = data
            return data

        except FileNotFoundError:
            print("No such 'devices.json'.")
            return
        except json.JSONDecodeError:
            print("Error to decodificate JSON format.")
            return


class LocalConnection(LocalModelTuya):
    def __init__(self):
        super().__init__()

    """
        TODO: tengo que modificar para que los dispositivos accedan a los 
        valores que pueden medir, y traer esa informacion, para almacenarla
    """
    def get_status_device_tuya(self, device_id: str):
        cred = LocalModelTuya().get_device_acces_data(device_id)
        print(cred)
        dev = tinytuya.OutletDevice(cred['id'],
                                    cred['ip'],
                                    cred['key'])
        dev.set_version(float(cred['version']))
        data = {}
        try:
            data = dev.status()
        except KeyboardInterrupt:
            print(
                "CANCEL: Interrupcion recibida por teclado %s [%s]."
                % (cred['id'], cred['ip'])
            )
        except Exception as e:
            print(f"ERROR: Ocurrió un error al obtener el estado del dispositivo: {e}")

        try:
            dps = data['dps']
            if dps:
                return dps
            else:
                print("Sin contenido DPS") #Logica de TUYA devices
                return
        except Exception as e:
            print(f"ERROR: Ocurrió un error al intentar leer la informacion del dispositivo: {e}")