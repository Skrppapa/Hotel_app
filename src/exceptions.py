class NabronirivalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NabronirivalException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(NabronirivalException):
    detail = "Не осталось свободных номеров"

