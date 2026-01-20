class Endpoints:
    BASE_URL = "https://stellarburgers.education-services.ru"

    CREATE_USER = f"{BASE_URL}/api/auth/register"
    LOGIN_USER = f"{BASE_URL}/api/auth/login"
    CREATE_ORDER = f"{BASE_URL}/api/orders"
    GET_INGREDIENTS = f"{BASE_URL}/api/ingredients"
    DELETE_USER = f"{BASE_URL}/api/auth/user"
