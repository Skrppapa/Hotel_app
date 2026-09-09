from datetime import date
from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache
from exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from services.hotels import HotelService
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить все отели")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(date(2026, 12, 1), description="Дата заезда"),
        date_to: date = Query(date(2026, 12, 10), description="Дата выезда")
):

    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to
    )

@router.get("/{hotel_id}", summary="Получение отеля по id")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

@router.post("", summary="Добавит отель")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples=
    {"1":
            {"summary": "Сочи",
             "value":
                {"title": "Отель Сочи 5 звезд у моря",
                 "location": "sochi_u_morya"}
             },
    "2":
            {"summary": "Дубай",
             "value":
                {"title": "Отель Дубай у фонтана",
                 "location": "Dubai_fontain"}
             },
    })):

    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновить данные отеля по ID")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные отеля по ID",
    description="<h1>Частичное обновление методом PATCH</h1>")

async def update_patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep
):
    await HotelService(db).update_patch_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель по ID")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
