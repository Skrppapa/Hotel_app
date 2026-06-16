from fastapi import APIRouter, HTTPException, Response
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=["Авторизация и Аутентификация"])

@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,  # Для помещения токена в куки
    db: DBDep
):
    """Аутентификация пользователя"""
    user = await db.users.get_user_with_hashed_password(email=data.email) # get_user_with_hashed_password Отдельный метод в репо. Где получаем юзера с хешированным паролем
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)  # Помещаем токен в куки после получения
    return {"access_token": access_token}


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep
):
    """Регистрация пользователя"""
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    """Извлечение и расшифровка токена из аутентифицированного пользователя (реализовано через Depends)"""
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Выход из системы"""
    response.delete_cookie("access_token")
    return {"status": "OK"}





