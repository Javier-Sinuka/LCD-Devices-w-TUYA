import devices_info


# # # Seteo del ID del dispositivo
# DEVICE_ID = devices_info.devices_list_id_and_custom_name()[0]['ID']
# print(DEVICE_ID)
# start_time = devices_info.cloud_info_devices.get('t') - 604800000
# # print(start_time)
# start_time_prueba = devices_info.calculate_previous_time(devices_info.cloud_info_devices.get('t'), 1, 'hour')
# print('Start time prueba: ' + str(start_time_prueba))
# # end_time = devices_info.cloud_info_devices.get('t')
# end_time = 1716935097862
# print('End time: ' + str(end_time))
# code = "cur_power"
# actual_time = devices_info.conversor_time_hours(1716942775676)
# print('Actual time: ' + str(actual_time))
# tiempo = devices_info.calculate_previous_time(1716935097862, 2, 'hour')
# print('Tiempo: ' + str(tiempo))

# end_time = 1716910462000 #28 de mayo del 2024 15:34:22
# DEVICE_ID = devices_info.devices_list_id_and_custom_name()[0]['ID']
# # print(DEVICE_ID)
# code = "cur_power"
# data = devices_info.get_status_list_week(DEVICE_ID, code, end_time)
# print(data)


# data = devices_info.get_status_list_day(DEVICE_ID, code, end_time, 20)
# print(data[1])
# print(data[0][::-1])

# Metodo para traer los eventos de encendido y apagado
# response = openapi.get("/v2.0/cloud/thing/{}/report-logs?codes={}&end_time={}&size=99&start_time={}".format(DEVICE_ID, code, end_time, start_time))
# response_2_testing = openapi.get("/v2.0/cloud/thing/{}/report-logs?codes={}&start_time={}&end_time={}&last_row_key=&size=20".format(DEVICE_ID, code, start_time, end_time))

# def event_time(response_value):
#     dict_event = {}
#     for log in response_value.get('result').get('logs'):
#         print(log.get('event_time'))
#         print(conversor_time_hours(log.get('event_time')) + ' ' + log.get('value'))
#
# event_time(response)

####################################################################################
############################# TESTING AREA #########################################

# print(openapi.get("/v1.0/devices/live-datas?date_type=week&product_id={}".format(DEVICE_ID)))
# print(devices_info.get_status_report_log(DEVICE_ID, code, 100, start_time, end_time))
# print(devices_info.calulate_average({23,23,22,25,23,23,25,26,99}))

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