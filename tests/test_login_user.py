import allure
from data.test_data import ErrorMessages
from helpers.data_generator import DataGenerator


@allure.epic("Stellar Burgers API")
@allure.feature("Авторизация пользователя")
class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    @allure.description("Тест проверяет успешную авторизацию с валидными учетными данными")
    def test_login_existing_user_success(self, setup_user, api_client):
        with allure.step("Создать тестового пользователя"):
            user_data, create_response, create_status = setup_user()
            assert create_status == 200, "Не удалось создать пользователя для теста"

        with allure.step("Подготовить данные для авторизации"):
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }

        with allure.step("Выполнить авторизацию"):
            response, status_code = api_client.login_user(login_data)

        with allure.step("Проверить успешную авторизацию"):
            assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
            assert response.success == True, "Поле success должно быть True"

        with allure.step("Проверить наличие токенов в ответе"):
            assert response.accessToken is not None, "В ответе должен быть accessToken"
            assert response.refreshToken is not None, "В ответе должен быть refreshToken"

        with allure.step("Проверить данные пользователя в ответе"):
            assert response.user is not None, "В ответе должна быть информация о пользователе"
            assert response.user["email"] == user_data["email"], "Email пользователя должен совпадать"
            assert response.user["name"] == user_data["name"], "Имя пользователя должно совпадать"

    @allure.title("Вход с неверным email")
    @allure.description("Тест проверяет ошибку при авторизации с неверным email")
    def test_login_with_invalid_email_fails(self, setup_user, api_client):
        with allure.step("Создать тестового пользователя"):
            user_data, create_response, create_status = setup_user()
            assert create_status == 200, "Не удалось создать пользователя для теста"

        with allure.step("Подготовить данные с неверным email"):
            login_data = {
                "email": "nonexistent9999@example.com",
                "password": user_data["password"]
            }

        with allure.step("Выполнить попытку авторизации"):
            response, status_code = api_client.login_user(login_data)

        with allure.step("Проверить ошибку авторизации"):
            assert status_code == 401, f"Ожидался статус 401, но получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INVALID_CREDENTIALS, \
                f"Ожидалось сообщение '{ErrorMessages.INVALID_CREDENTIALS}', но получено '{response.message}'"

    @allure.title("Вход с неверным паролем")
    @allure.description("Тест проверяет ошибку при авторизации с неверным паролем")
    def test_login_with_invalid_password_fails(self, setup_user, api_client):
        with allure.step("Создать тестового пользователя"):
            user_data, create_response, create_status = setup_user()
            assert create_status == 200, "Не удалось создать пользователя для теста"

        with allure.step("Подготовить данные с неверным паролем"):
            login_data = {
                "email": user_data["email"],
                "password": "wrongpassword123456"
            }

        with allure.step("Выполнить попытку авторизации"):
            response, status_code = api_client.login_user(login_data)

        with allure.step("Проверить ошибку авторизации"):
            assert status_code == 401, f"Ожидался статус 401, но получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INVALID_CREDENTIALS, \
                f"Ожидалось сообщение '{ErrorMessages.INVALID_CREDENTIALS}', но получено '{response.message}'"

    @allure.title("Вход с неверным email и паролем")
    @allure.description("Тест проверяет ошибку при авторизации с неверными email и паролем")
    def test_login_with_invalid_email_and_password_fails(self, api_client):
        with allure.step("Сгенерировать полностью невалидные учетные данные"):
            data_generator = DataGenerator()
            invalid_credentials = data_generator.generate_invalid_credentials()

        with allure.step("Выполнить попытку авторизации"):
            response, status_code = api_client.login_user(invalid_credentials)

        with allure.step("Проверить ошибку авторизации"):
            assert status_code == 401, f"Ожидался статус 401, но получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INVALID_CREDENTIALS, \
                f"Ожидалось сообщение '{ErrorMessages.INVALID_CREDENTIALS}', но получено '{response.message}'"

    @allure.title("Вход без пароля")
    @allure.description("Тест проверяет ошибку при авторизации без пароля")
    def test_login_without_password_fails(self, setup_user, api_client):
        with allure.step("Создать тестового пользователя"):
            user_data, create_response, create_status = setup_user()
            assert create_status == 200, "Не удалось создать пользователя для теста"

        with allure.step("Подготовить данные без пароля"):
            login_data = {
                "email": user_data["email"]
            }

        with allure.step("Выполнить попытку авторизации"):
            response, status_code = api_client.login_user(login_data)

        with allure.step("Проверить ошибку авторизации"):
            assert status_code == 401, f"Ожидался статус 401, но получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INVALID_CREDENTIALS, \
                f"Ожидалось сообщение '{ErrorMessages.INVALID_CREDENTIALS}', но получено '{response.message}'"

    @allure.title("Вход без email")
    @allure.description("Тест проверяет ошибку при авторизации без email")
    def test_login_without_email_fails(self, setup_user, api_client):
        with allure.step("Создать тестового пользователя"):
            user_data, create_response, create_status = setup_user()
            assert create_status == 200, "Не удалось создать пользователя для теста"

        with allure.step("Подготовить данные без email"):
            login_data = {
                "password": user_data["password"]
            }

        with allure.step("Выполнить попытку авторизации"):
            response, status_code = api_client.login_user(login_data)

        with allure.step("Проверить ошибку авторизации"):
            assert status_code == 401, f"Ожидался статус 401, но получен {status_code}"
            assert response.success == False, "Поле success должно быть False"
            assert response.message == ErrorMessages.INVALID_CREDENTIALS, \
                f"Ожидалось сообщение '{ErrorMessages.INVALID_CREDENTIALS}', но получено '{response.message}'"