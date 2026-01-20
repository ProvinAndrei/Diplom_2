# Diplom_2

Автотесты для API сервиса Stellar Burgers.

## Структура проекта

- tests/ # Тесты
- api/ # Эндпоинты и модели ответов
- data/ # Тестовые данные
- helpers/ # API клиент и генераторы данных

## Тестируемые эндпоинты:
- Создание пользователя (/api/auth/register)
- Логин пользователя (/api/auth/login)
- Создание заказа (/api/orders)

## Установка

```bash
pip install -r requirements.txt

# Все тесты
pytest tests/ -v

# С генерацией Allure отчета
pytest tests/ --alluredir=allure-results
allure serve allure-results