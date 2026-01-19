import allure
import pytest
from conftest import SimpleResponse, ErrorMessages


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
            assert status_code == 200
            assert response.success is True
            assert response.name is not None
            assert response.order is not None
            assert "number" in response.order

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет, что заказ можно создать без авторизации")
    def test_create_order_without_auth_success(self, api_client, valid_ingredients):
        with allure.step("Убедиться, что токен авторизации отсутствует"):
            api_client.set_token(None)

        with allure.step("Создать заказ без авторизации"):
            order_data = {"ingredients": valid_ingredients}
            api_response, status_code = api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить успешное создание заказа"):
            assert status_code == 200
            assert response.success is True
            assert response.name is not None
            assert response.order is not None

    @allure.title("Создание заказа с разным количеством ингредиентов")
    @allure.description("Тест проверяет создание заказа с 1 и 2+ ингредиентами")
    @pytest.mark.parametrize("ingredient_count, description", [
        (1, "Один ингредиент"),
        (2, "Два ингредиента"),
    ])
    def test_create_order_with_various_ingredient_counts(
        self, authorized_api_client, valid_ingredients, ingredient_count, description
    ):
        """Заменил test_create_order_with_different_ingredient_counts 
           и test_create_order_with_max_ingredients"""
        with allure.step(description):
            ingredients = valid_ingredients[:ingredient_count]
            order_data = {"ingredients": ingredients}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить успешное создание"):
            assert status_code == 200
            assert response.success is True
            assert response.order is not None

    @allure.title("Создание заказа без ингредиентов (негативный)")
    @allure.description("Тест проверяет ошибку при создании заказа с пустым списком ингредиентов")
    def test_create_order_without_ingredients_fails(self, authorized_api_client):
        with allure.step("Попытаться создать заказ с пустым списком ингредиентов"):
            order_data = {"ingredients": []}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить ошибку валидации"):
            assert status_code == 400
            assert response.success is False
            assert response.message == ErrorMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа без поля ingredients (негативный)")
    @allure.description("Тест проверяет ошибку при создании заказа без поля ingredients")
    def test_create_order_without_ingredients_field_fails(self, authorized_api_client):
        with allure.step("Попытаться создать заказ без поля ingredients"):
            order_data = {}  # Отсутствует поле ingredients
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить ошибку валидации"):
            assert status_code == 400
            assert response.success is False
            assert response.message == ErrorMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиентов (негативный)")
    @allure.description("Тест проверяет обработку невалидных ID ингредиентов")
    def test_create_order_with_invalid_ingredients_hash(self, authorized_api_client):
        with allure.step("Попытаться создать заказ с невалидными ингредиентами"):
            invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
            order_data = {"ingredients": invalid_ingredients}
            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить ошибку сервера"):
            # API может возвращать 500 или 400
            assert status_code in [400, 500]
            assert response.success is False

    @allure.title("Параметризованный тест различных невалидных данных")
    @allure.description("Объединяет несколько негативных сценариев")
    def test_create_order_with_various_invalid_data(
        self, authorized_api_client, invalid_ingredients_data
    ):
        test_data = invalid_ingredients_data

        with allure.step(f"Попытаться создать заказ с данными: {test_data}"):
            order_data = {}
            if test_data is not None:
                order_data["ingredients"] = test_data

            api_response, status_code = authorized_api_client.create_order(order_data)
            response = SimpleResponse(api_response)

        with allure.step("Проверить обработку невалидных данных"):
            assert status_code in [400, 500]
            assert response.success is False
