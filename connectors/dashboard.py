import requests
import os
from connectors.utils.modifiers import ModifiersConnector

connector = ModifiersConnector()

class DashboardManager(ModifiersConnector):
    token = ''

    def __init__(self):
        super().__init__()

    def send_to_dashboard(self, token: str, time_to_send: int):
        url = "http://api.tago.io/data"
        base_url = os.getenv("UVICORN_ADDRESS")
        data = connector.get_values_devices_kwh(base_url, time_to_send)
        for d in data:
            requests.post(url=url, headers={'Authorization': token}, json=d)
