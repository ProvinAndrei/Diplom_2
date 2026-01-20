class SimpleResponse:
    """Модель для работы с ответами ApiClient в тестах"""

    def __init__(self, api_response):
        # ApiClient возвращает объект с атрибутами
        # Просто копируем их
        self.success = getattr(api_response, 'success', None)
        self.name = getattr(api_response, 'name', None)
        self.order = getattr(api_response, 'order', None)
        self.message = getattr(api_response, 'message', None)
        self.accessToken = getattr(api_response, 'accessToken', None)
        self.refreshToken = getattr(api_response, 'refreshToken', None)
        self.user = getattr(api_response, 'user', None)

    def __repr__(self):
        return f"SimpleResponse(success={self.success}, name={self.name})"
