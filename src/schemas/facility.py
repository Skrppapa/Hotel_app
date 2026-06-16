from pydantic import BaseModel, ConfigDict

class FacilitiesAdd(BaseModel):
    title: str


class Facility(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilitiesPatch(BaseModel):
    title: str | None = None


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int