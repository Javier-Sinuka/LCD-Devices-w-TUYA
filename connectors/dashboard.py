import requests
from connectors.utils.modifiers import ModifiersConnector

connector = ModifiersConnector()

def send2Tago():
    token = ""
    url = "http://api.tago.io/data"
    data = connector.get_values_devices_kwh("http://127.0.0.1:8001")
    requests.post(url=url, headers={'Authorization':token}, json=data )

send2Tago()
