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
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Get Devices
response_test = openapi.get("/v2.0/cloud/thing/device?page_size=5")

def devices_list_id():
    variable_test = response_test.get('result')
    devices_list = []

    for element in variable_test:
        devices_list.append(element['id'])

    return devices_list

def device_specific_value(device_id, required_parameter):
    value_parameter = ''

    for element in response_test.get('result'):
        if element['id'] == device_id:
            value_parameter = element[required_parameter]

    return value_parameter

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
    Metodo que calcula el valor en milisegundos, realizando la resta de los dias ingresados
    al valor en formato de milisegundos, retornando dicho valor en el mismo formato (milisegundos)
"""
def calculate_previous_time(timestamp_ms, days_substract):
    calulate_timestamp_ms = datetime.fromtimestamp(timestamp_ms/1000) - timedelta(days=days_substract)
    return (int(calulate_timestamp_ms.timestamp() * 1000))

# Seteo del ID del dispositivo
DEVICE_ID = devices_list_id()[1]
print(DEVICE_ID)
start_time = response_test.get('t') - 604800000
# print(start_time)
start_time_prueba = calculate_previous_time(response_test.get('t'), 7)
# print('Start time prueba: ' + str(start_time_prueba))
end_time = response_test.get('t')
# print('End time: ' + str(end_time))
code = "switch_1"
code_test = "switch_led_1"
actual_time = conversor_time_hours(response_test.get('t'))
# print('Actual time: ' + str(actual_time))

# print('Info relevante: ' + '\n' +
#       'Device ID: ' + DEVICE_ID + '\n' +
#       'Conversor time - t valor: ' + conversor_time_hours(response_test.get('t')) + '\n' +
#       'Start time: ' + (response_test.get('t') - 604800000) + '\n' +
#       'Start time - 7 days minous (another method): ' + str(start_time_prueba) + '\n' +
#       'End time: ' + str(end_time) + '\n' +
#       'Actual time: ' + str(actual_time) + '\n'
#       )

# Metodo para traer los eventos de encendido y apagado
response = openapi.get("/v2.0/cloud/thing/{}/report-logs?codes={}&end_time={}&size=99&start_time={}".format(DEVICE_ID, code, end_time, start_time))

# response_2_testing = openapi.get("/v2.0/cloud/thing/{}/report-logs?codes={}&start_time={}&end_time={}&last_row_key=&size=20".format(DEVICE_ID, code, start_time, end_time))

def event_time(response_value):
    dict_event = {}
    for log in response_value.get('result').get('logs'):
        print(log.get('event_time'))
        print(conversor_time_hours(log.get('event_time')) + ' ' + log.get('value'))

event_time(response)

####################################################################################
############################# TESTING AREA #########################################

# print(openapi.get("/v1.0/devices/live-datas?date_type=week&product_id={}".format(DEVICE_ID)))

# Metodo para ver la cantidad de dispositivos activos en el timepo indicado
# ("Count the number of daily active devices" -> https://developer.tuya.com/en/docs/cloud/data-service?id=K95zu0f66bv4m#title-50-Count%20the%20number%20of%20daily%20active%20devices)
# response = openapi.get("/v1.0/devices/live-datas?date_type=week&product_id=".format(DEVICE_ID))

# Trae la informacion de todos los dispositivos, pero mediante Industry y no Samrt Home
# response = openapi.get("/v1.3/iot-03/devices")

# response = openapi.get("/v1.0/iot-03/energy/electricity/devices/nodes/statistics-trend?energy_action=consume&statisticsType=day&startTime=20240524&endTime=20240525&containChilds=false&device_ids=eb75e00e75c89084femtye,eba16cb6e8116961166ft4")


####################################################################################
####################################################################################


#############################################################################################
################################# TUYA INFO DEFAULT #########################################
#############################################################################################

# # Call APIs from Tuya
# # Get the device information
# response = openapi.get("/v1.0/iot-03/devices/{}".format(DEVICE_ID))
#
# # Get the instruction set of the device
# response = openapi.get("/v1.0/iot-03/devices/{}/functions".format(DEVICE_ID))
# print(response)
#
# # Send commands
# commands = {'commands': [{'code': 'switch_1', 'value': True}]}
# openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
#
# Get the status of a single device
# response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))
# response = openapi.get("/v2.0/cloud/thing/{}".format(DEVICE_ID))

# # Init Message Queue
# open_pulsar = TuyaOpenPulsar(
# 	ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD
# )
# # Add Message Queue listener
# open_pulsar.add_message_listener(lambda msg: print(f"---\nexample receive: {msg}"))
#
# # Start Message Queue
# open_pulsar.start()
#
# input()
# # Stop Message Queue
# open_pulsar.stop()