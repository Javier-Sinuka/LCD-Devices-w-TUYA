import requests, json

class ApiClient():
    def __init__(self):
        pass

    def post_element(self, url: str, payload: json):
        response = requests.post(url, json=payload)
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.json()

    def get_element(self, url: str):
        response = requests.get(url)
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.json()