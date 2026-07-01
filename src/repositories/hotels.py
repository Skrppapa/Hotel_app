from datetime import date
from sqlalchemy import select
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset
    ) -> list(Hotel):

        rooms_ids_for_get = rooms_ids_for_booking(date_from, date_to)

        hotels_ids_for_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_for_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_for_get))

        if location:
            query = (
                query
                .filter(HotelsOrm.location
                .ilike(f"%{location.strip()}%")) # Метод ilike - не зависит от регистра. strip() - чистит пробелы до и после
            ) # Еще есть чуть более чистый вариант без f строки через icontains(): query = query.filter(HotelsOrm.location.icontains(location.strip()))

        if title:
            query = (
                query
                .filter(HotelsOrm.title
                .ilike(f"%{title.strip()}%"))
            )

        query = (
            query
            .limit(limit)
            .offset(offset)  # offset - Смещение
        )

        result = await self.session.execute(query)
        # Возвращается не список отелей, а итератор! (Точнее список кортежей. В каждом кортеже 1 объект из бд (одна запись))

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]




