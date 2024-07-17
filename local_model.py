import time
from datetime import datetime, timedelta, timezone
import json
import tinytuya
# import tuyapower
import numpy
# tinytuya.set_debug(True)

class LocalModel:
    __devices_acces = []
    __devices_data = []

    def __init__(self, file_name='acces.json'):
        self.file_name = file_name
        self.__devices_data = {}
        self.__devices_acces = {}
        self.safe_to_json()

    """
        Metodo para almacenar las credenciales de los dispositivos presentes en la red local
        en un archivo JSON.
    """
    def safe_to_json(self):
        try:
            with open('devices.json', 'r') as file:
                data = json.load(file)
            with open('devices.json', 'r') as file:
                self.__devices_data = json.load(file)

        except FileNotFoundError:
            print("El archivo 'devices.json' no se encontró.")
            return
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON.")
            return

        for element in data:
            if 'id' in element and 'ip' in element and 'key' in element:
                self.__devices_acces[element['name']] = {
                    'id': element['id'],
                    'ip': element['ip'],
                    'key': element['key'],
                    'version': element['version']
                }
            else:
                print(f"Elemento inválido encontrado y omitido: {element}")

        with open(self.file_name, 'w') as json_file:
            json.dump(self.__devices_acces, json_file, indent=4)

    """
        Representacion en formato ano-mes-dia-hora-minuto-segundo de un valor en milisegundos
    """
    def conversor_time_hours(self, time_r: int, format='YY:MM:DD'):
        utc_date = datetime.fromtimestamp((time_r / 1000.0), tz=timezone.utc)
        utc_hour = timezone(timedelta(hours=-3))
        utc_time = utc_date.astimezone(utc_hour)
        date = ''
        if format == 'HH':
            date = utc_time.strftime('%H')
        elif format == 'YY:MM:DD':
            date = utc_time.strftime('%Y-%m-%d')
        return date

    """
        Metodo que devuelve el tiempo actual en milisegundos.
    """
    def get_actual_time(self):
        return int(time.time() * 1000)

    """
        Metodo que calcula el valor en milisegundos, realizando la resta respecto al valor ingresado ('day' o 'hour')
        al valor en formato de milisegundos, retornando dicho valor en el mismo formato (milisegundos)
    """
    def calculate_previous_time(self, timestamp_ms, substract, tipe: str):
        calculate_timestamp_ms = 0
        try:
            if tipe == 'hour':
                calculate_timestamp_ms = datetime.fromtimestamp(timestamp_ms / 1000) - timedelta(hours=substract)
            elif tipe == 'day':
                calculate_timestamp_ms = datetime.fromtimestamp(timestamp_ms / 1000) - timedelta(days=substract)
            return (int(calculate_timestamp_ms.timestamp() * 1000))
        except ValueError:
            print("Ingrese valor correcto respecto al tipo a retornar: " + '\n' +
                  'day' + '\n' +
                  'hour' + '\n')

    """
        Metodo que devuelve la informacion de acceso local de todos los dispositivos.
    """
    def get_all_acces_data(self):
        # try:
        #     with open('acces.json', 'r') as file:
        #         data = json.load(file)
        #     return data
        # except Exception:
        #     print("Error al abrir archivo con todos los datos de acceso.")
        #     return
        return self.__devices_acces

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
        Metodo que devuelve los valores solicitados de TODOS LOS DISPOSITIVOS existentes en la red,
        los cuales son solicitados mediante la lista ingresada.
    """
    def get_devices_list_info(self, list_elements):
        devices_list = []
        content_list = []
        for element in self.__devices_data:
            for content in list_elements:
                content_list.append({content: element[content]})
            devices_list.append(content_list)
            content_list = []
        return devices_list

    """
        Devuelve una lista con la TODA la informacion asociada a un dispositivo especifico, 
        ingresando unicamente su id.
    """
    def get_device_individual_info(self, device_id):
        dev_list = []
        for element in self.__devices_data:
            if element['id'] == device_id:
                dev_list.append(element)
        return dev_list


class LocalConection(LocalModel):
    def __init__(self):
        super().__init__()

    def get_status_device(self, device_id):
        cred = LocalModel().get_device_acces_data(device_id)
        print(cred)
        dev = tinytuya.OutletDevice(cred['id'],
                                    cred['ip'],
                                    cred['key'], )
        dev.set_version(cred['version'])
        data = {}
        device_status = {}
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
            if data:
                dps = data['dps']
                if "19" in dps:  # Hacer logica para el agregado de la corriente
                    device_status['current'] = dps['18']
                    device_status['power'] = dps['19']
                    device_status['voltage'] = dps['20']
                    device_status['time'] = self.get_actual_time()
                elif "1" in dps and "40" in dps:  # Logica para el switch
                    device_status['switch_value'] = dps['1']
                    device_status['time'] = self.get_actual_time()
                else:
                    print()
            return device_status
        except Exception as e:
            print(f"ERROR: Ocurrió un error al intentar leer la informacion del dispositivo: {e}")

# e = LocalConection()
# print(e.get_status_device(e.get_all_acces_data()["Enchufe dispenser 1"].get('id')))
# print(e.get_device_acces_data(""))
# t = LocalConection()
# t.get_status_device('')
# d = tinytuya.OutletDevice(dev_id=DEVICE_ID,
#     address=IP_ADDRESS,
#     local_key=LOCAL_KEY,
#     version=3.3)


#################################################################################

# (on, w, mA, V, err) = tuyapower.deviceInfo(DEVICE_ID, IP_ADDRESS, LOCAL_KEY, DEV_TYPE)
#
# data = d.status()
# d.add_dps_to_request()
# Show status and state of first controlled switch on device
# print('Dictionary %r' % data)

# d.turn_off()
# time.sleep(2)
# d.turn_on()



