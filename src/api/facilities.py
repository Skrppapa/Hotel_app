from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facility import Facility, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список всех удобств")
async def get_facilities(db: DBDep) -> list[Facility]:
    return await db.facilities.get_all()


@router.post("", summary="Добавить удобство")
async def add_facilities(db: DBDep, facilities_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facilities_data)
    await db.commit()

    return {"status": "OK", "data": facility}
