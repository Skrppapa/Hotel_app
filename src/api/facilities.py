from fastapi import APIRouter, Body
from services.facilities import FacilitiesService
from src.api.dependencies import DBDep
from src.schemas.facility import Facility, FacilitiesAdd
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep) -> list[Facility]:
    return await FacilitiesService(db).get_all()


@router.post("", summary="Добавить удобство")
async def add_facilities(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facility = await FacilitiesService(db).create_facility(facilities_data)
    return {"status": "OK", "data": facility}
