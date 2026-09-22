from fastapi import APIRouter, Response
from exceptions import EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException, UserAlreadyExistsException, \
    UserEmailAlreadyExistsHTTPException
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,  # Для помещения токена в куки
    db: DBDep
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)  # Помещаем токен в куки после получения
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    """Извлечение и расшифровка токена из аутентифицированного пользователя (реализовано через Depends)"""
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Выход из системы"""
    response.delete_cookie("access_token")
    return {"status": "OK"}





