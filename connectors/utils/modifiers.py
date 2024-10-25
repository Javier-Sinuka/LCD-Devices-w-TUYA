import json
import os
from connectors.utils.base import BaseConnector
from datetime import datetime, timedelta
import numpy as np
import calendar
import locale
from collections import defaultdict

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class ModifiersConnector(BaseConnector):
    def __init__(self):
        super().__init__()

    #TODO Abstaerse y no generar dependencia de una ruta especifica
    def get_content_file(self, name_file):
        try:
            file_path = os.path.join(os.path.dirname(__file__), name_file)
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError as e:
            print(f"Error load file: {e}")

    def processed_data(self, fetch_values, device_name: str, attribute_name: str, data_elements, time_to_send: int):
        dashboard_data = []

        if fetch_values is None:
            try:
                dashboard_data.append({
                    "variable": f"consumo_{device_name.lower().replace(' ', '_').replace('-', '_')}",
                    "value": "NULL",
                    "unit": "kWh",
                })
                return dashboard_data
            except Exception as e:
                print(f"Error fetching data and send NULL: {e}")

        elif (attribute_name == 'cur_power'):
            try:
                data = self.analyze_kwh_values(fetch_values, time_to_send)
                for d in data:
                    dashboard_data.append({
                        "variable": f"consumo_{device_name.lower().replace(' ', '_').replace('-', '_')}",
                        "value": d['value'],
                        "unit": "kWh",
                    })
                return dashboard_data
            except Exception as e:
                print(f"Error cur_power: {e}")

        elif (attribute_name == 'switch_1'):
            try:
                data = self.analyze_switch_values(fetch_values, time_to_send)
                #Esta cuenta se encarga de calcular el consumo de la linea del switch
                #Obteniendo primero el consumo total en whatts, pasandolo a kW, y luego
                #transformando este valor en kWh medido en el rango pedido.
                consume_kwh = ((data_elements['amount_leds'] * data_elements['watt_consume']) / 1000) * (time_to_send/60)
                for d in data:
                    dashboard_data.append({
                        "variable": f"consumo_{device_name.lower().replace(' ', '_').replace('-', '_')}",
                        "value": round(consume_kwh, 4) if d['value'] == 'True' else 0,
                        "unit": "kWh",
                    })
                return dashboard_data
            except Exception as e:
                print(f"Error switch_1: {e}")

    def get_elements(self, base_url: str, device_id: int, attribute_id: int, start_date: datetime, end_date: datetime, data_elements, time_to_send:int):
        attribute_name = self.get_attribute_name(base_url, attribute_id)
        device_name = (self.get_device_name(base_url, device_id)).lower()
        fetch_values = self.fetch_values_by_device_and_attribute(base_url, device_id, attribute_id, start_date, end_date)
        return self.processed_data(fetch_values, device_name, attribute_name, data_elements, time_to_send)

    def get_values_devices_kwh(self, base_url: str, time_to_send: int):
        data_reading_devices = self.get_content_file('local_leds.json')
        send_data = []
        current_time = datetime.now()
        end_time = current_time
        start_time = (current_time - timedelta(minutes=time_to_send-1))
        totally_consume = 0.0
        beginning_month = False
        
        for data in data_reading_devices:
            device_id = self.get_id_for_name_device(base_url, data)
            attribute_id = self.get_id_for_name_attribute(base_url, data_reading_devices[data]['type'])
            element = self.get_elements(base_url, device_id, attribute_id, start_time, end_time, data_reading_devices[data], time_to_send)
            # Tener en cuenta que esto metodo envia los consumos mensuales de los distintos dispositivos presentes
            # y no realiza una discriminacion de si esto se pide o no, lo hace cuando es el primero de cada mes.
            if current_time.day == 1:
                beginning_month = True
                end_time_m = start_time.replace(hour=0, minute=0)
                month = start_time.month -1
                start_time_m = datetime(start_time.year, month, start_time.day, hour=0, minute=0)
                month_consume = self.monthly_device_consumption(base_url, device_id, attribute_id, start_time_m, end_time_m)
                dashboard_data = []
                dashboard_data.append({
                    "variable": f"consumo_mensual_{data.lower().replace(' ', '_').replace('-', '_')}",
                    "value": month_consume,
                    "unit": "kWh",
                    "metadata": {
                        "variable" : f"consumo_{calendar.month_name[month]}_{data.lower().replace(' ', '_').replace('-', '_')}"
                    }
                })
                send_data.extend(dashboard_data)
                totally_consume += month_consume
                
            if element is not None:
                send_data.extend(element)

        if beginning_month:
            print("Entro")
            send_data.extend([{
                "variable": f"consumo_total_lcd",
                "value": totally_consume,
                "unit": "kWh",
            }])
        print(send_data)
        return send_data

    def monthly_device_consumption(self, base_url: str, device_id: int, attribute_id: int, start_date: datetime, end_date: datetime):
        """
        Metodo que calula el consumo de los dispositivos dentro de un mes, comenzando desde el
        primero de cada mes, devolviendo el valor referido a este en formato de kwh.
        """
        data_reading_devices = self.get_content_file('local_leds.json')
        attribute_name = self.get_attribute_name(base_url, attribute_id)
        data = self.fetch_values_by_device_and_attribute(base_url, device_id, attribute_id, start_date, end_date)

        if attribute_name == 'switch_1':
            new_data = self.group_by_hour(data)
            value = []

            for data in new_data:
                dat = self.analyze_switch_values(new_data[data], 60)
                value.append(dat)

            device_name = self.get_device_name(base_url, device_id)
            consume_kwh = data_reading_devices[device_name]['amount_leds'] * data_reading_devices[device_name]['watt_consume']
            return self.calculate_switich_totally(value, consume_kwh)

        elif attribute_name == 'cur_power':
            data_modified = self.monthly_values_sum_kwh_no_switch(data)
            return data_modified

    def calculate_switich_totally(self, list, value_led: int):
        """
        Calculo del consumo medido por los switches.
        Como el valor obtenido es un valor booleano, que representa si el dispositivo estuvo
        encendido en esa hora (True) o apagado (False), este se toma como 1, y se multiplica
        con el valor de 'valued_led', el cual es el valor asociado a la cantidad de leds que posee
        dicho swicth en su gobernanza, multiplicado por el valor de consumo de KWH del led de dicha linea.
        """
        counter = 0.0
        for element in list:
            if element[0]['value'] == True:
                counter += 1 * value_led
        return (counter/1000)

    def monthly_values_sum_kwh_no_switch(self, data):
        """
        Funcion que devuelve la suma de todos los valores asociados a la lista
        de elementos pasados como parametros (estos elementos estan asociados a los
        consumos en un determinado tiempo, teniendo de datos el valor de su tiempo de medicion
        'timestamp' y el valor asociado a esa medicion 'value', de la cual se utiliza este ultimo
        para realizar la sumatoria total de estos)
        """
        values = []
        for item in data:
            value = item.get('value')
            try:
                values.append(float(value))
            except (ValueError, TypeError):
                print(f"Error value incorrect: {value}")
        total_value = (np.sum(values) if values else 0)/10000
        return float(total_value)

    def group_by_hour(self, data):
        """
        Funcion que agrupa una serie de elementos pasados como parametros en grupos en base
        a rangos horarios, agrupando los elementos dentro franjas horarias con diferencia de una hora.
        Esto es muy util, para poder utilizar despues dicha informacion para ser procesada
        y obtener los consumos de los elementos asociados a esta.
        """
        by_hour = defaultdict(list)
        for item in data:
            timestamp = datetime.fromisoformat(item['timestamp'])
            specific_hour = timestamp.strftime('%Y-%m-%dT%H')
            by_hour[specific_hour].append(item)
        return dict(by_hour)