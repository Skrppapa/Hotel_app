from datetime import date
from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache
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
        date_from: date = Query(example = "2026-08-01"),
        date_to: date = Query(example = "2026-08-10")
):

    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location = location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}", summary="Получение отеля по id")
async def get_hotel(hotel_id: int, db: DBDep):
        return await db.hotels.get_one_or_none(id=hotel_id)



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

    hotel = await db.hotels.add(hotel_data)
    await db.commit()  # Коммит указываем явно, т.к. указали expire_on_commit=False

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновить данные отеля по ID")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id = hotel_id)
    await db.commit()   # Коммит делаем внутри ручки!!!
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
    await db.hotels.edit(hotel_data, exclude_unset=True, id = hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель по ID")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id = hotel_id)
    await db.commit()
    return {"status": "OK"}
