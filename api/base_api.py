import requests


class BaseAPI:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    def post(self, endpoint, json=None):
        return requests.post(endpoint, json=json, headers=self.headers)

    def get(self, endpoint, params=None):
        return requests.get(endpoint, params=params, headers=self.headers)

    def patch(self, endpoint, json=None):
        return requests.patch(endpoint, json=json, headers=self.headers)

    def delete(self, endpoint):
        return requests.delete(endpoint, headers=self.headers)