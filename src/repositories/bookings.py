from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd
from src.schemas.rooms import RoomAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_check(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]


    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_for_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_for_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        # Если id нашего номера находится в списке rooms_ids_to_book значит можем забронировать
        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(500) # Пока что 500 ошибка

