import json
import os
from connectors.utils.base import BaseConnector
from datetime import datetime, timedelta

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

    def get_elements(self, base_url: str, device_id: int, attribute_id: int, start_date: datetime, end_date: datetime, data_elements):
        attribute_name = self.get_attribute_name(base_url, attribute_id)
        device_name = (self.get_device_name(base_url, device_id)).lower()
        dashboard_data = []
        fetch_values = self.fetch_values_by_device_and_attribute(base_url, device_id, attribute_id, start_date, end_date)

        if (attribute_name == 'cur_power'):
            try:
                data = self.analyze_kwh_values(fetch_values)
                for d in data:
                    dashboard_data.append({
                        "variable": f"consumo_{device_name.lower().replace(' ', '_')}",
                        "value": d['value'],
                        "time": d['timestamp'],
                        "unit": "kWh",
                    })
                return dashboard_data
            except Exception as e:
                print(f"Error get_elements: {e}")

        elif (attribute_name == 'switch_1'):
            try:
                data = self.analyze_switch_values(fetch_values)
                consume_kwh = data_elements['amount_leds'] * data_elements['watt_consume']
                for d in data:
                    dashboard_data.append({
                        "variable": f"consumo_{device_name.lower().replace(' ', '_')}",
                        "unit": "kWh",
                        "value": consume_kwh if d['value'] else 0
                    })
                return dashboard_data
            except Exception as e:
                print(f"Error fetching data: {e}")

    def get_values_devices_kwh(self, base_url: str):
        data_reading_devices = self.get_content_file('local_leds.json')
        send_data = []
        current_time = datetime.now()
        end_time = current_time.replace(minute=0, second=0, microsecond=0)
        start_time = (current_time - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        for data in data_reading_devices:
            device_id = self.get_id_for_name_device(base_url, data)
            attribute_id = self.get_id_for_name_attribute(base_url, data_reading_devices[data]['type'])
            send_data.append({self.get_elements(base_url, device_id, attribute_id, start_time, end_time, data_reading_devices[data])})
        return send_data