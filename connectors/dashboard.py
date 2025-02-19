import requests
from connectors.utils.modifiers import ModifiersConnector

connector = ModifiersConnector()

class DashboardManager(ModifiersConnector):
    token = ''

    def __init__(self):
        super().__init__()

    def send_to_dashboard(self, token: str, time_to_send: int):
        url = "http://api.tago.io/data"
        data = connector.get_values_devices_kwh("http://127.0.0.1:8001", time_to_send)
        for d in data:
            requests.post(url=url, headers={'Authorization': token}, json=d)
