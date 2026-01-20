from api.base_api import BaseAPI
from api.endpoints import Endpoints
from api.responses import BaseResponse, UserCreationResponse, LoginResponse, OrderCreationResponse


class ApiClient(BaseAPI):
    def __init__(self):
        super().__init__()
        self.token = None

    def set_token(self, token):
        self.token = token
        if token:
            self.headers["Authorization"] = token
        else:
            self.headers.pop("Authorization", None)

    def create_user(self, user_data):
        response = self.post(Endpoints.CREATE_USER, json=user_data)
        return self._parse_response(response, UserCreationResponse)

    def login_user(self, login_data):
        response = self.post(Endpoints.LOGIN_USER, json=login_data)
        return self._parse_response(response, LoginResponse)

    def get_ingredients(self):
        response = self.get(Endpoints.GET_INGREDIENTS)
        return response

    def create_order(self, order_data):
        response = self.post(Endpoints.CREATE_ORDER, json=order_data)
        return self._parse_response(response, OrderCreationResponse)

    def delete_user(self, access_token):
        original_headers = self.headers.copy()
        self.headers["Authorization"] = access_token

        response = self.delete(Endpoints.DELETE_USER)

        self.headers = original_headers
        return response.status_code

    def _parse_response(self, response, response_class):
        try:
            response_data = response.json()
            return response_class(**response_data), response.status_code
        except ValueError:
            return BaseResponse(success=False, message="Invalid response format"), response.status_code
