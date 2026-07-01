from pydantic import BaseModel, ConfigDict, EmailStr

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

# Будет переходная модель, сначала получаем исходный пароль, а после хешируем
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

# Наследуемся именно от BaseModel, что бы не отдавать на клиент пароль ни в каком виде
class User(BaseModel):
    id: int
    email: EmailStr


    model_config = ConfigDict(from_attributes=True)

# Отдельная схема - под конкретный случай при аутентификации существующего пользователя, что бы проверить пароль на истинность
class UserWithHashedPassword(User):
    hashed_password: str