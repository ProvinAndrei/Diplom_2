import pytest
from helpers.api_client import ApiClient
from helpers.data_generator import DataGenerator


@pytest.fixture
def setup_user():
    """Фикстура для создания пользователя с автоматическим удалением после теста"""
    client = ApiClient()  # Создаем клиент внутри фикстуры
    created_users = []

    def _create_user(user_data=None):
        """Создает пользователя и возвращает данные"""
        if user_data is None:
            data_generator = DataGenerator()
            user_data = data_generator.generate_user_data()

        response, status_code = client.create_user(user_data)
        if status_code == 200:
            # Сохраняем данные для cleanup
            created_users.append((user_data, response.accessToken))
            return user_data, response, status_code
        return user_data, response, status_code

    yield _create_user

    # Cleanup: удаляем всех созданных пользователей после теста
    for user_data, access_token in created_users:
        if access_token:
            client.delete_user(access_token)


@pytest.fixture
def authenticated_user(setup_user):
    """Фикстура для создания и авторизации пользователя"""
    user_data, response, status_code = setup_user()

    if status_code == 200:
        return user_data, response.accessToken
    else:
        pytest.fail(f"Не удалось создать пользователя для теста: {status_code}")


@pytest.fixture
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов с API"""
    client = ApiClient()  # Создаем клиент здесь
    response = client.get_ingredients()

    if response.status_code != 200:
        pytest.fail(f"Не удалось получить ингредиенты: {response.status_code}")

    data = response.json()
    if not data.get("success") or "data" not in data:
        pytest.fail("Некорректный ответ от API ингредиентов")

    # Берем ID первых 2 валидных ингредиентов
    ingredients = [ingredient["_id"] for ingredient in data["data"][:2]]
    return ingredients


@pytest.fixture
def authorized_api_client(authenticated_user):
    """
    API клиент с установленным токеном авторизации.
    Устраняет дублирование кода в тестах.
    """
    user_data, access_token = authenticated_user
    client = ApiClient()
    client.set_token(access_token)
    return client
