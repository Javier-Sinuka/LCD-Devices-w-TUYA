import requests
from connectors.utils.modifiers import ModifiersConnector

connector = ModifiersConnector()

class DashboardManager(ModifiersConnector):
    token = ''

    def __init__(self):
        super().__init__()

    def send_to_tago(self,  token: str):
        url = "http://api.tago.io/data"
        data = connector.get_values_devices_kwh("http://127.0.0.1:8001")
        requests.post(url=url, headers={'Authorization': token}, json=data)
