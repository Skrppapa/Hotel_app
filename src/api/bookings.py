from fastapi import APIRouter
from exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from services.bookings import BookingsService
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get("/me", summary="Получить все бронирования пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingsService(db).get_my_bookings(user_id)


@router.post("", summary="Добавить бронирования")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest
):

    try:
        booking = await BookingsService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
