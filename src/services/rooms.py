from datetime import date

from exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    RoomNotFoundException
from schemas.facility import RoomFacilityAdd
from schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch, Room
from services.base import BaseService
from services.hotels import HotelService


class RoomsService(BaseService):

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date):

            check_date_to_after_date_from(date_from, date_to)
            return await self.db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


    async def get_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)


    async def create_room(
            self,
            hotel_id: int,
            room_data: RoomAddRequest
    ):

            try:
                await self.db.hotels.get_one(id=hotel_id)  # Проверяем что отель существует
            except ObjectNotFoundException as ex:
                raise HotelNotFoundException from ex

            # Приняли данные от пользователя, приняли данные внутри системы о hotel_id и склеили их в одну схему (см. схему RoomAddRequest)
            _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
            room = await self.db.rooms.add(_room_data)

            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facility_ids
                ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
            await self.db.commit()  # Только здесь делаем коммит. Мы в рамках одной транзакции делаем 2 запроса (на добавление номера и на добавление удобств) и только потом коммитим.


    async def edit_room(
            self, 
            hotel_id: int,
            room_id: int,
            room_data: RoomAddRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facility(room_id, facilities_id=room_data.facility_ids)
        await self.db.commit()


    async def update_patch_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facility(room_id, facilities_id=_room_data_dict["facilities_ids"])
        await self.db.commit()

    async def delete_room(
            self,
            hotel_id: int, 
            room_id: int
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()


    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(room_id)  # Проверяем что номер существует
        except ObjectNotFoundException:
            raise RoomNotFoundException