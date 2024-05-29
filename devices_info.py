import json
import logging
from datetime import datetime, timedelta, timezone
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tuya_connector import (
	TuyaOpenAPI,
	TuyaOpenPulsar,
	TuyaCloudPulsarTopic,
    TUYA_LOGGER,
)

with open('acces.json', 'r') as file:
    config = json.load(file)

ACCESS_ID = config['ACCESS_ID']
ACCESS_KEY = config['ACCESS_KEY']
API_ENDPOINT = config['API_ENDPOINT']
MQ_ENDPOINT = config['MQ_ENDPOINT']

# Enable debug log
# TUYA_LOGGER.setLevel(logging.DEBUG)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Get Devices
cloud_info_devices = openapi.get("/v2.0/cloud/thing/device?page_size=5")
result_list = cloud_info_devices.get('result')

"""
    Representacion en formato ano-mes-dia-hora-minuto-segundo de un valor en milisegundos
"""
def conversor_time_hours(time):
    utc_date = datetime.fromtimestamp((time/1000.0), tz=timezone.utc)
    utc_hour = timezone(timedelta(hours=-3))
    utc_time = utc_date.astimezone(utc_hour)
    date = utc_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return date

"""
    Metodo que calcula el valor en milisegundos, realizando la resta respecto al valor ingresado ('day' o 'hour')
    al valor en formato de milisegundos, retornando dicho valor en el mismo formato (milisegundos)
"""
def calculate_previous_time(timestamp_ms, substract, tipe:str):
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
    Metodo que devuelve una lista con los ID de los dispositivos y su customName asociado
"""
def devices_list_id_and_custom_name():
    devices_list = []
    for element in result_list:
        devices_list.append({'Custom Name': element['customName'], 'ID': element['id']})
    return devices_list

def device_specific_value(device_id, required_parameter):
    value_parameter = ''
    for element in result_list:
        if element['id'] == device_id:
            value_parameter = element[required_parameter]
    return value_parameter

"""
    Metodo que devuelve los customName de todos los dispositivos registrados
"""
def get_custom_name_list():
    custom_name_list = []
    for element in result_list:
        custom_name_list.append(element['customName'])
    return custom_name_list

"""
    Obtencion ID mediante customName (nombre puesto al dispositivo a la hora de inicializarlo)  
"""
def get_device_id(customName):
    device_id = ''
    for element in result_list:
        if element['customName'] == customName:
            device_id = element['id']
    return device_id

"""
    Metodo que expone los distintos codigos de lectura respecto al ID del dispositivo ingresado,
    dichos codigos pueden ser utilizados para realizar una peticion de valores referidos a 
    dicho codigo.
"""
def get_status_codes_device_list(device_id):
    response = openapi.get("/v1.0/iot-03/devices/{}/specification".format(device_id))
    codes_device = response.get('result').get('status')
    codes_list = []
    for code in codes_device:
        codes_list.append(code.get('code'))
    return codes_list

"""
    Metodo que calcula el promedio de los los elementos ingresados por una lista y 
    devuelve dicho valor en formato entero (sin decimales)
"""
def calculate_average(list: list):
    average = 0
    for element in list:
        if element is not None:
            average += element
    return (int(average/len(list)))

"""
    Metodo que devuelve el "Status Report Log" de un dispositivo y su codigo asociado.
    
    :params
    device_id: str (ID del dispositivo),
    code: str (Valor a obtener),
    size: int (Cantidad de elementos a retornar en la lista),
    start_time: int (En milisegundos, tiempo de inicio de la toma de datos),
    end_time: int (En milisegundos, tiempo de finalizacion de la toma de datos).
    
    :return
    Lista de elementos solicitados.
"""
def get_status_report_log(device_id, code, size: int, start_time: int, end_time: int):
    response = openapi.get("/v2.0/cloud/thing/{}/report-logs?codes={}&end_time={}&size={}&start_time={}".format(device_id, code, end_time, size, start_time)).get('result').get('logs')
    return response


"""
    Metodo que devuelve una lista con 24 elementos especificados por el 'code' ingresado,
    dichos valores son los equivalentes a 24hs antes del tiempo ingresado en 'end_time'.

    :params
    device_id: str (ID del dispositivo),
    code: str (Valor a obtener),
    end_time: int (En milisegundos, tiempo de finalizacion de la toma de datos)

    :return
    Lista con elementos que contienen los siguientes parametros:
        'event_time' -> Referencia al tiempo en que en que fue tomada la medicion (valor en milisegundos)
        'value' -> Promedio respecto al valor solicitado (code)
    Dichos elementos seran los relacionados al codigo ingresado.
"""


def get_status_list_day(device_id, code, end_time: int):
    status_list = []
    for i in range(24):
        new_end_time = calculate_previous_time(end_time, i, 'hour')
        list_values = get_status_report_log(device_id, code, 100, calculate_previous_time(new_end_time, 1, 'hour'), new_end_time)
        print(list_values)
        # status_list.append()
    return status_list

# """
#     Metodo que devuelve una lista con los elementos especificados por el 'code' ingresado.
#     Se puede especificar el tamano de la lista (minimo 1 a  maximo de 100 elementos).
#     Ademas, dichos elementos cuentan con dos parametros: 'event_time': int, 'value': int.
#
#     :params
#     device_id: str (ID del dispositivo),
#     code: str (Valor a obtener),
#     size: int (Cantidad de elementos a retornar en la lista),
#     start_time: int (En milisegundos, tiempo de inicio de la toma de datos),
#     end_time: int (En milisegundos, tiempo de finalizacion de la toma de datos).
#
#     :return
#     Lista con elementos que contienen los siguientes parametros:
#         'event_time' -> Referencia al tiempo en que en que fue tomada la medicion (valor en milisegundos)
#         'value' -> Referencia al valor solicitado (code)
#     Dichos elementos seran los relacionados al codigo ingresado.
# """
# def get_status_list(device_id, code, size: int, start_time: int, end_time: int):
#     status_list = []
#     return status_list

# """
#     Metodo que devuelve una lista con los elementos especificados por el 'code' ingresado.
#     Opciones validas de time_return:
#         day -> Devuelve una lista con 24 elementos que cuenta con los parametros 'event_time': int, 'value': int.
#         week -> Devuelve una lista con 7 elementos que cuenta con los parametros 'event_time': int, 'value': int.
#     Se toma el valor ingresado en end_time, y se le resta el valor correspondiente a la peticion (day=ultimas 24hs
#     medidas, week=ultimos 7 dias).
#
#     :params
#     device_id: str (ID del dispositivo),
#     code: str (Valor a obtener),
#     end_time: int (En milisegundos, tiempo de finalizacion de la toma de datos),
#     time_return: str (day -> Ultimas 24hs [lista de 24 elementos], week -> Ultimos 7 dias [lista de 7 elementos])
#
#     :return
#     Lista con elementos que contienen los siguientes parametros:
#         'event_time' -> Referencia al tiempo en que en que fue tomada la medicion (valor en milisegundos)
#         'value' -> Promedio respecto al valor solicitado (code)
#     Dichos elementos seran los relacionados al codigo ingresado.
# """
# def get_status_list_day_week(device_id, code, end_time: int, time_return: str):
#     status_list = []
#     try:
#         if time_return == 'week':
#
#         elif time_return == 'day':
#
#     except ValueError:
#         print("Ingrese valor correcto respecto a time_return" + '\n' +
#               'day' + '\n' +
#               'week' + '\n')
#
#     return status_list

