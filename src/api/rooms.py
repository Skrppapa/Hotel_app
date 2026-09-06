from fastapi import Body, APIRouter, Query, HTTPException
from exceptions import ConflictOfEqualDateException, ConflictDateException, ObjectNotFoundException, \
    check_date_to_after_date_from, HotelNotFoundHTTPException, RoomNotFoundHTTPException
from src.api.dependencies import DBDep
from src.schemas.facility import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from datetime import date

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(default="2026-08-01"),
        date_to: date = Query(default="2026-08-10")):

    check_date_to_after_date_from(date_from, date_to)
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    if not room:
        raise RoomNotFoundHTTPException
    return room


@router.post("/{hotel_id}", summary="Добавит номер")
async def create_room(db: DBDep,
                      hotel_id: int,
                      room_data: RoomAddRequest = Body()):
    try:
        await db.hotels.get_one(id=hotel_id)  # Проверяем что отель существует
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        # Приняли данные от пользователя, приняли данные внутри системы о hotel_id и склеили их в одну схему (см. схему RoomAddRequest)
        _room_data = RoomAdd(hotel_id = hotel_id, **room_data.model_dump())
        room = await db.rooms.add(_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Указанного отеля не существует")

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facility_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit() # Только здесь делаем коммит. Мы в рамках одной транзакции делаем 2 запроса (на добавление номера и на добавление удобств) и только потом коммитим.
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить данные номера по ID")
async def edit_room(hotel_id: int,
                    room_id: int,
                    room_data: RoomAddRequest,
                    db: DBDep):

    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id = room_id)
    await db.rooms_facilities.set_room_facility(room_id, facilities_id = room_data.facility_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частично обновить данные номера по ID",
    description="<h1>Частичное обновление методом PATCH</h1>")

async def update_patch_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facility(room_id, facilities_id = _room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер по ID")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.get_one(id=room_id)  # Проверяем что номер существует
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}