from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm
from sqlalchemy.orm import selectinload
from src.schemas.rooms import RoomWithRels
from datetime import date



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        rooms_ids_for_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)  # Подгружаем саму модель
            .options(selectinload(self.model.facilities)) # Подгружаем удобства через relationships
            .filter(RoomsOrm.id.in_(rooms_ids_for_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]


    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model)



















