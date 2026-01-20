import allure
import pytest
from helpers.api_client import ApiClient
from helpers.models import SimpleResponse
from data.test_data import ErrorMessages


@allure.epic("Stellar_Burgers_API")
@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест проверяет успешное создание заказа с авторизацией")
    def test_create_order_with_auth_success(self, authorized_api_client, valid_ingredients):
        """Тест покрывает: с авторизацией + с ингредиентами"""
        with allure.step("Создать заказ с валидными ингредиентами"):
            order_data = {"ingredients": valid_ingredients}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить успешное создание заказа"):
            assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
            assert response.success is True, "Поле success должно быть True"
            assert response.name is not None, "В ответе должно быть имя заказа"
            assert response.order is not None, "В ответе должна быть информация о заказе"
            assert "number" in response.order, "В заказе должен быть номер"

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет, что заказ можно создать без авторизации")
    def test_create_order_without_auth_success(self, valid_ingredients):
        with allure.step("Создать API клиент без авторизации"):
            api_client = ApiClient()
            api_client.set_token(None)

        with allure.step("Создать заказ без авторизации"):
            order_data = {"ingredients": valid_ingredients}
            api_response, status_code = api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить успешное создание заказа"):
            assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
            assert response.success is True, "Поле success должно быть True"
            assert response.name is not None, "В ответе должно быть имя заказа"
            assert response.order is not None, "В ответе должна быть информация о заказе"

    @allure.title("Создание заказа с разным количеством ингредиентов")
    @allure.description("Тест проверяет создание заказа с 1 и 2+ ингредиентами")
    @pytest.mark.parametrize("ingredient_count, description", [
        (1, "Один ингредиент"),
        (2, "Два ингредиента"),
    ])
    def test_create_order_with_various_ingredient_counts(
        self, authorized_api_client, valid_ingredients, ingredient_count, description
    ):
        with allure.step(description):
            ingredients = valid_ingredients[:ingredient_count]
            order_data = {"ingredients": ingredients}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить успешное создание"):
            assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
            assert response.success is True, "Поле success должно быть True"
            assert response.order is not None, "В ответе должна быть информация о заказе"

    @allure.title("Создание заказа без ингредиентов (негативный)")
    @allure.description("Тест проверяет ошибку при создании заказа с пустым списком ингредиентов")
    def test_create_order_without_ingredients_fails(self, authorized_api_client):
        with allure.step("Попытаться создать заказ с пустым списком ингредиентов"):
            order_data = {"ingredients": []}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить ошибку валидации"):
            assert status_code == 400, f"Ожидался статус 400, получен {status_code}"
            assert response.success is False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INGREDIENTS_REQUIRED, \
                f"Ожидалось сообщение '{ErrorMessages.INGREDIENTS_REQUIRED}', получено '{response.message}'"

    @allure.title("Создание заказа без поля ingredients (негативный)")
    @allure.description("Тест проверяет ошибку при создании заказа без поля ingredients")
    def test_create_order_without_ingredients_field_fails(self, authorized_api_client):
        with allure.step("Попытаться создать заказ без поля ingredients"):
            order_data = {}  # Отсутствует поле ingredients
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить ошибку валидации"):
            assert status_code == 400, f"Ожидался статус 400, получен {status_code}"
            assert response.success is False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INGREDIENTS_REQUIRED, \
                f"Ожидалось сообщение '{ErrorMessages.INGREDIENTS_REQUIRED}', получено '{response.message}'"

    @allure.title("Создание заказа с неверным хешем ингредиентов (негативный)")
    @allure.description("Тест проверяет обработку невалидных ID ингредиентов")
    def test_create_order_with_invalid_ingredients_hash(self, authorized_api_client):
        with allure.step("Попытаться создать заказ с невалидными ингредиентами"):
            invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
            order_data = {"ingredients": invalid_ingredients}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить ошибку сервера"):
            # Уточняем ожидаемый статус (зависит от API)
            assert status_code == 500, f"Ожидался статус 500 для невалидных ингредиентов, получен {status_code}"
            assert response.success is False, "Поле success должно быть False"

    # РАЗДЕЛИЛИ ПАРАМЕТРИЗОВАННЫЙ ТЕСТ НА ОТДЕЛЬНЫЕ АТОМАРНЫЕ ТЕСТЫ

    @allure.title("Создание заказа с пустым списком ингредиентов")
    @allure.description("Тест проверяет ошибку при создании заказа с пустым списком ингредиентов")
    def test_create_order_with_empty_list(self, authorized_api_client):
        """Отдельный атомарный тест для пустого списка"""
        order_data = {"ingredients": []}
        api_response, status_code = authorized_api_client.create_order(order_data)
        response = SimpleResponse(api_response)

        assert status_code == 400, f"Ожидался статус 400 для пустого списка, получен {status_code}"
        assert response.success is False, "Поле success должно быть False"
        assert response.message == ErrorMessages.INGREDIENTS_REQUIRED, \
            f"Ожидалось сообщение '{ErrorMessages.INGREDIENTS_REQUIRED}', получено '{response.message}'"

    @allure.title("Создание заказа без поля ingredients")
    @allure.description("Тест проверяет ошибку при создании заказа без поля ingredients")
    def test_create_order_with_missing_field(self, authorized_api_client):
        """Отдельный атомарный тест для отсутствия поля"""
        order_data = {}  # Нет поля ingredients
        api_response, status_code = authorized_api_client.create_order(order_data)
        response = SimpleResponse(api_response)

        assert status_code == 400, f"Ожидался статус 400 для отсутствия поля, получен {status_code}"
        assert response.success is False, "Поле success должно быть False"
        assert response.message == ErrorMessages.INGREDIENTS_REQUIRED, \
            f"Ожидалось сообщение '{ErrorMessages.INGREDIENTS_REQUIRED}', получено '{response.message}'"

    @allure.title("Создание заказа с невалидным хешем ингредиента")
    @allure.description("Тест проверяет обработку невалидного ID ингредиента")
    def test_create_order_with_invalid_hash(self, authorized_api_client):
        """Отдельный атомарный тест для невалидного хеша"""
        order_data = {"ingredients": ["invalid_hash_1"]}
        api_response, status_code = authorized_api_client.create_order(order_data)
        response = SimpleResponse(api_response)

        # Уточняем ожидаемый статус для невалидного хеша
        assert status_code == 500, f"Ожидался статус 500 для невалидного хеша, получен {status_code}"
        assert response.success is False, "Поле success должно быть False"
