import pytest
from helpers.api_client import ApiClient
from helpers.data_generator import DataGenerator


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return ApiClient()


@pytest.fixture
def setup_user(api_client):
    """Фикстура для создания пользователя с автоматическим удалением после теста"""
    created_users = []

    def _create_user(user_data=None):
        """Создает пользователя и возвращает данные"""
        if user_data is None:
            data_generator = DataGenerator()
            user_data = data_generator.generate_user_data()

        response, status_code = api_client.create_user(user_data)
        if status_code == 200:
            # Сохраняем данные для cleanup
            created_users.append((user_data, response.accessToken))
            return user_data, response, status_code
        return user_data, response, status_code

    yield _create_user

    # Cleanup: удаляем всех созданных пользователей после теста
    for user_data, access_token in created_users:
        if access_token:
            api_client.delete_user(access_token)


@pytest.fixture
def authenticated_user(setup_user):
    """Фикстура для создания и авторизации пользователя"""
    user_data, response, status_code = setup_user()

    if status_code == 200:
        return user_data, response.accessToken
    else:
        pytest.fail(f"Не удалось создать пользователя для теста: {status_code}")


@pytest.fixture
def valid_ingredients(api_client):
    """Фикстура для получения валидных ингредиентов с API"""
    response = api_client.get_ingredients()
    assert response.status_code == 200, f"Не удалось получить ингредиенты: {response.status_code}"
    data = response.json()
    assert data["success"] == True, "API должно вернуть success: true"
    assert "data" in data, "В ответе должен быть ключ 'data'"
    # Берем ID первых 2 валидных ингредиентов
    ingredients = [ingredient["_id"] for ingredient in data["data"][:2]]
    return ingredients


@pytest.fixture
def authorized_api_client(api_client, authenticated_user):
    """
    API клиент с установленным токеном авторизации.
    Устраняет дублирование кода в тестах.
    """
    user_data, access_token = authenticated_user
    api_client.set_token(access_token)
    return api_client


@pytest.fixture(params=[
    [],  # Пустой список (без ингредиентов)
    None,  # Отсутствие поля ingredients
    ["invalid_hash_1"],  # Невалидный хеш ингредиентов
])
def invalid_ingredients_data(request):
    """
    Различные невалидные данные для ингредиентов.
    Используется в параметризованном тесте.
    """
    return request.param


class SimpleResponse:
    """Модель для работы с ответами ApiClient"""

    def __init__(self, api_response):
        # ApiClient возвращает объект с атрибутами
        # Просто копируем их
        self.success = getattr(api_response, 'success', None)
        self.name = getattr(api_response, 'name', None)
        self.order = getattr(api_response, 'order', None)
        self.message = getattr(api_response, 'message', None)
        self.accessToken = getattr(api_response, 'accessToken', None)
        self.user = getattr(api_response, 'user', None)

    def __repr__(self):
        return f"SimpleResponse(success={self.success}, name={self.name})"


class ErrorMessages:
    """Класс с сообщениями об ошибках API"""

    # Сообщения для заказов
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
