class UserData:
    REQUIRED_FIELDS = ["email", "password", "name"]
    PASSWORD = "password"
    # Для теста существующего пользователя (будет создан в фикстуре)
    EXISTING_USER_EMAIL = "existing_user@example.com"


class OrderData:
    # Валидные ингредиенты из документации
    VALID_INGREDIENTS = ["60d3463f7034a000269f45e7", "60d3463f7034a000269f45e9"]
    INVALID_INGREDIENTS = ["invalid_ingredient_1"]


class ErrorMessages:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELD = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    UNAUTHORIZED = "You should be authorised"
