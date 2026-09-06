from datetime import date
from fastapi import HTTPException


class NabronirivalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NabronirivalException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(NabronirivalException):
    detail = "Не осталось свободных номеров"

class ObjectAlreadyExistsException(NabronirivalException):
    detail = "Объект уже существует в системе"

class ConflictDateException(NabronirivalException):
    detail = "Дата заезда не может быть позже даты выезда"

class ConflictOfEqualDateException(NabronirivalException):
    detail = "Дата заезда не может быть равна дате выезда"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата выезда не может быть позже даты заезда")




class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"
