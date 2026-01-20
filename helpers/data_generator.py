import random
import string
from data.test_data import UserData


class DataGenerator:
    @staticmethod
    def generate_unique_email():
        """Генерация уникального email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"test_user_{random_string}@example.com"

    @staticmethod
    def generate_unique_name():
        """Генерация уникального имени"""
        random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"TestUser_{random_string}"

    @staticmethod
    def generate_user_data(email=None, password=None, name=None):
        """Генерация данных для нового пользователя"""
        return {
            "email": email or DataGenerator.generate_unique_email(),
            "password": password or UserData.PASSWORD,
            "name": name or DataGenerator.generate_unique_name()
        }

    @staticmethod
    def generate_user_without_field(missing_field):
        """Генерация данных пользователя с пропущенным обязательным полем"""
        user_data = DataGenerator.generate_user_data()
        user_data.pop(missing_field)
        return user_data

    @staticmethod
    def generate_invalid_credentials():
        """Генерация невалидных учетных данных"""
        return {
            "email": "invalid@example.ya",
            "password": "wrongpassword_999"
        }
