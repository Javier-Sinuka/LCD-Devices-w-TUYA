import numpy
import local_model

local_model = local_model.LocalModel()

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
def get_event_list_day(device_id, code, end_time: int):
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

            status_list.append({'event_time': local_model.conversor_time_hours(new_end_time, 'HH'),
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
def get_event_list_week(device_id, code, end_time: int):
    status_list = []
    for i in range(7):
        new_end_time = end_time - (i*86400000)
        total_value = get_event_list_day(device_id, code, new_end_time)[1]
        status_list.append({'event_time': local_model.conversor_time_hours(new_end_time), 'value': total_value})
    return status_list