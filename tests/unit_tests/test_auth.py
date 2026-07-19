from src.services.auth import AuthService


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token  # Убеждаемся что токен существует
    assert isinstance(jwt_token, str)  # Убеждаемся что токен имеет тип str (как и указано в методе)