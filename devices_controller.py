import json
from datetime import datetime, timedelta, timezone
import sys
import os
import numpy

import cloud_model

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

with open('devices.json', 'r') as file:
    data = json.load(file)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Get Devices Info
result_list = data

"""
    Representacion en formato ano-mes-dia-hora-minuto-segundo de un valor en milisegundos
"""
def conversor_time_hours(time, format='YY:MM:DD'):
    utc_date = datetime.fromtimestamp((time/1000.0), tz=timezone.utc)
    utc_hour = timezone(timedelta(hours=-3))
    utc_time = utc_date.astimezone(utc_hour)
    date = ''
    if format == 'HH':
        date = utc_time.strftime('%H')
    elif format == 'YY:MM:DD':
        date = utc_time.strftime('%Y-%m-%d')
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
    Metodo que devuelve los valores del dispositivo, solicitados en 'list_elements'
"""
def get_device_info_list(list_elements):
    devices_list = []
    content_list = []
    for element in result_list:
        for content in list_elements:
            content_list.append({content: element[content]})
        devices_list.append(content_list)
        content_list = []
    return devices_list

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
    Metodo que devuelve una lista con 24 elementos especificados por el 'code' ingresado,
    dichos valores son los equivalentes a 24hs previo del tiempo ingresado en 'end_time'.
    
    :params
    device_id: str (ID del dispositivo),
    code: str (Valor a obtener),
    end_time: int (En milisegundos, tiempo de finalizacion de la toma de datos)
    precision: int (Cantidad de muestras a tomar en el intervalo de tiempo, en este caso, entre las distintas horas)

    :return
    Lista con elementos que contienen los siguientes parametros:
        'event_time' -> Referencia al tiempo en que en que fue tomada la medicion (valor en milisegundos)
        'value' -> Promedio respecto al valor solicitado (code)
    Dichos elementos seran los relacionados al codigo ingresado.
"""
def get_power_list_day(device_id, code, end_time: int):
    status_list = []
    list_values = []
    total_value = 0

    for i in range(24):
        new_end_time = end_time - (i * 3600000)
        values = cloud_model.get_devices_log(device_id, (new_end_time-3600000), new_end_time)['result']['logs']
        if values is not None and len(values) > 0:
            for element in values:
                if 'code' in element and element['code'] == code:
                    list_values.append(float(element['value']))
                else:
                    list_values.append(float(0))

            if list_values:
                average = numpy.mean(list_values)
            else:
                average = 0

            status_list.append({'event_time': conversor_time_hours(new_end_time, 'HH'),
                                'value': float(format((average/10000), ".2g"))})
            list_values.clear()

    for element in status_list:
        total_value += element['value']
    print(status_list)
    return status_list, total_value

"""
    Metodo que devuelve una lista con 7 elementos especificados por el 'code' ingresado,
    dichos valores son los equivalentes a 7 previos del dia ingresado ingresado en 'end_time'.

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
def get_power_list_week(device_id, code, end_time: int):
    status_list = []
    for i in range(7):
        new_end_time = end_time - (i*86400000)
        total_value = get_power_list_day(device_id, code, new_end_time)[1]
        status_list.append({'event_time': conversor_time_hours(new_end_time), 'value': total_value})
    return status_list