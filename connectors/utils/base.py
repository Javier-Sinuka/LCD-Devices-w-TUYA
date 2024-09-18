import requests
from datetime import datetime, timedelta
from collections import defaultdict

class BaseConnector:
    def __init__(self):
        pass

    def fetch_values_by_device_and_attribute(self, base_url: str, device_id: int, attribute_id: int, start_date: datetime, end_date: datetime):
        endpoint = f"{base_url}/values/devices/{device_id}/attributes/{attribute_id}/values"
        # params = {
        #     "start_date": start_date.replace(minute=0, second=0, microsecond=0).isoformat(),
        #     "end_date": end_date.replace(minute=0, second=0, microsecond=0).isoformat(),
        # }
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def get_id_for_name_device(self, base_url: str, name_device:str):
        endpoint = f"{base_url}/devices/id_by_name/{name_device}"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def get_id_for_name_attribute(self, base_url: str, name_device:str):
        endpoint = f"{base_url}/attributes/id_by_name/{name_device}"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def get_attribute_name(self, base_url: str, attribute_id:int):
        endpoint = f"{base_url}/attributes/{attribute_id}/name"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def get_device_name(self, base_url: str, device_id:int):
        endpoint = f"{base_url}/devices/name/{device_id}"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def analyze_switch_values(self, data):
        """
        Analiza los cambios de valores por hora, determinando el valor predominante basado en la duración.

        Parameters:
            data (list): Lista de diccionarios con 'value' (boolean) y 'timestamp' (datetime).

        Returns:
            list: Lista de diccionarios con el valor predominante y la hora (timestamp).
        """
        hourly_values = defaultdict(lambda: {"True": timedelta(0), "False": timedelta(0)})

        for i in range(len(data) - 1):
            if isinstance(data[i]['timestamp'], str):
                for d in data:
                    d['timestamp'] = datetime.fromisoformat(d['timestamp'])

            current = data[i]
            next_item = data[i + 1]
            hour = current['timestamp'].replace(minute=0, second=0, microsecond=0)

            duration = next_item['timestamp'] - current['timestamp']
            value_str = str(current['value'])
            hourly_values[hour][value_str] += duration

        last_item = data[-1]
        last_hour = last_item['timestamp'].replace(minute=0, second=0, microsecond=0)
        end_of_hour = last_hour + timedelta(hours=1)
        hourly_values[last_hour][str(last_item['value'])] += end_of_hour - last_item['timestamp']

        result = []
        for hour, durations in sorted(hourly_values.items()):
            dominant_value = "True" if durations["True"] > durations["False"] else "False"
            result.append({"value": dominant_value == "True", "timestamp": hour.hour})
        return result

    def analyze_kwh_values(self, data, time_to_send: int):
        """
        Calcula los valores en kWh por hora basado en datos de consumo en mW.

        Parameters:
            data (list): Lista de diccionarios con 'value' (mW como string) y 'timestamp' (datetime).

        Returns:
            list: Lista de diccionarios con el valor en kWh y la hora correspondiente.
        """

        if time_to_send == 60:
            hourly_values = defaultdict(float)

            for i in range(len(data) - 1):
                if isinstance(data[i]['timestamp'], str):
                    for d in data:
                        d['timestamp'] = datetime.fromisoformat(d['timestamp'])

                current = data[i]
                next_item = data[i + 1]
                hour = current['timestamp'].replace(minute=0, second=0, microsecond=0)
                duration_in_hours = (next_item['timestamp'] - current['timestamp']).total_seconds() / 3600
                value_in_kwh = (float(current['value']) / 10000)
                hourly_values[hour] += value_in_kwh * duration_in_hours

            last_item = data[-1]
            last_hour = last_item['timestamp'].replace(minute=0, second=0, microsecond=0)
            end_of_hour = last_hour + timedelta(hours=1)
            duration_in_hours = (end_of_hour - last_item['timestamp']).total_seconds() / 3600
            value_in_kwh = (float(last_item['value']) / 1000) / 1000
            hourly_values[last_hour] += value_in_kwh * duration_in_hours

            result = [{"value": round(value, 4), "timestamp": hour.hour} for hour, value in
                      sorted(hourly_values.items())]
            return result

        else:
            average = 0
            timestamp = ''
            for i in data:
                value = i['value']
                average += int(value)
                timestamp = i['timestamp']
            average /= len(data)
            result = [{"value": round((average/1000), 4), "timestamp": timestamp}]
            return result