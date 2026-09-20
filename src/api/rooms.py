from fastapi import Body, APIRouter, Query
from services.rooms import RoomsService
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from datetime import date
from exceptions import HotelNotFoundHTTPException, RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(default="2026-08-01"),
        date_to: date = Query(default="2026-08-10")
):
    return await RoomsService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):
    try:
        return await RoomsService(db).get_room(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}", summary="Добавит номер")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body()
):
    try:
        room = await RoomsService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:   # В сервисе выкидываем именно эту ошибку, здесь ее отлавливам
        raise HotelNotFoundHTTPException   # А raise уже HTTP

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить данные номера по ID")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep
):
    await RoomsService(db).edit_room(hotel_id, room_id, room_data)
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
    await RoomsService(db).update_patch_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер по ID")
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):
    await RoomsService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}