import requests
from api.endpoints import Endpoints


class BaseAPI:
    def __init__(self):
        self.base_url = Endpoints.BASE_URL
        self.headers = {"Content-Type": "application/json"}

    def post(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, json=json, headers=self.headers)

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, params=params, headers=self.headers)

    def patch(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        return requests.patch(url, json=json, headers=self.headers)

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        return requests.delete(url, headers=self.headers)
