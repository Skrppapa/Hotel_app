import json
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facility import Facility, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список всех удобств")
async def get_facilities(db: DBDep) -> list[Facility]:
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        print("GO TO DB")
        facilities = await db.facilities.get_all()  # Получаем удобства из бд в виде списка схем Pydantic
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]  # Преобразуем в список словариков
        facilities_json = json.dumps(facilities_schemas) # Преобразуем в json
        await redis_manager.set("facilities", facilities_json, 10) # Запишем в кэш
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post("", summary="Добавить удобство")
async def add_facilities(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facilities_data)
    await db.commit()

    return {"status": "OK", "data": facility}
