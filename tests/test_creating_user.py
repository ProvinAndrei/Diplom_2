import allure
import pytest
from data.test_data import UserData, ErrorMessages
from helpers.api_client import ApiClient  # <-- ДОБАВИТЬ импорт
from helpers.data_generator import DataGenerator


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание нового пользователя с валидными данными")
    def test_create_unique_user_success(self, setup_user):
        with allure.step("Сгенерировать данные для нового пользователя"):
            user_data, response, status_code = setup_user()

        with allure.step("Проверить успешное создание пользователя"):
            assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
            assert response.success == True, "Поле success должно быть True"

        with allure.step("Проверить наличие токенов в ответе"):
            assert response.accessToken is not None, "В ответе должен быть accessToken"
            assert response.refreshToken is not None, "В ответе должен быть refreshToken"

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Тест проверяет ошибку при попытке создать уже существующего пользователя")
    def test_create_existing_user_fails(self, setup_user):  # <-- УБРАТЬ api_client из параметров
        with allure.step("Создать первого пользователя"):
            user_data, first_response, first_status = setup_user()
            assert first_status == 200, "Не удалось создать пользователя для теста"

        with allure.step("Попытаться создать пользователя с теми же данными повторно"):
            api_client = ApiClient()  # <-- СОЗДАТЬ КЛИЕНТ ЗДЕСЬ
            response, status_code = api_client.create_user(user_data)

        with allure.step("Проверить ошибку дублирования пользователя"):
            assert status_code == 403, f"Ожидался статус 403, получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.USER_ALREADY_EXISTS, \
                f"Ожидалось сообщение '{ErrorMessages.USER_ALREADY_EXISTS}', получено '{response.message}'"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Тест проверяет ошибку при создании пользователя без обязательных полей")
    @pytest.mark.parametrize("missing_field", UserData.REQUIRED_FIELDS)
    def test_create_user_without_required_field(self, missing_field):  # <-- УБРАТЬ api_client из параметров
        with allure.step(f"Сгенерировать данные пользователя без поля '{missing_field}'"):
            data_generator = DataGenerator()
            user_data = data_generator.generate_user_without_field(missing_field)

        with allure.step("Попытаться создать пользователя с неполными данными"):
            api_client = ApiClient()  # <-- СОЗДАТЬ КЛИЕНТ ЗДЕСЬ
            response, status_code = api_client.create_user(user_data)

        with allure.step("Проверить ошибку валидации"):
            assert status_code == 403, f"Ожидался статус 403, получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.REQUIRED_FIELD, \
                f"Ожидалось сообщение '{ErrorMessages.REQUIRED_FIELD}', получено '{response.message}'"
