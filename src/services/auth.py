from datetime import timedelta, datetime, timezone
from exceptions import IncorrectTokenException, ObjectAlreadyExistsException, UserAlreadyExistsException, \
    EmailNotRegisteredException, IncorrectPasswordException
from schemas.users import UserRequestAdd, UserAdd
from services.base import BaseService
from src.config import settings
from pwdlib import PasswordHash
import jwt

class AuthService(BaseService):

    pwd_context = PasswordHash.recommended()

    # Упрощенная функция из документации
    def create_access_token(self, data: dict) -> str:
        """Выдача токена пользователю при аутентификации"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        """Хэширование пароля"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """Проверка валидности пароля (проверяется в хешированном виде)"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        """Расшифровка токена"""
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException


    async def register_user(self, data: UserRequestAdd):
        """Регистрация пользователя"""

        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAdd):
        """Аутентификация пользователя"""

        user = await self.db.users.get_user_with_hashed_password(email=data.email) # get_user_with_hashed_password Отдельный метод в репо.
        if not user:                                                               # Где получаем юзера с хешированным паролем
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
