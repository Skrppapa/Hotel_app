from pydantic import BaseModel, ConfigDict
from src.schemas.facility import Facility


# Здесь создал отдельную схему RoomAddRequest, где исключил параметр hotel_id. Мы не должны запрашивать его у пользователя.
# Внутри приложения уже используется схема с hotel_id
# Так мы меньше данных гоняем по сети
# С Patch та же история

class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facility_ids: list[int] = []

class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

    hotel_id: int

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

    hotel_id: int | None = None
