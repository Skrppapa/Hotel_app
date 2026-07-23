from datetime import date

from src.schemas.bookings import BookingAdd, BookingPatch


async def test_booking_crud(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    booking_data = BookingAdd(
        room_id = room_id,
        user_id = user_id,
        date_from = date(year=2026, month=12, day=20),  # Передаем именно в формате date т.к. тестируем работу бд, а не api
        date_to = date(year=2027, month=1, day=1),
        price = 100
    )
    new_booking = await db.bookings.add(booking_data)

    # Получить бронь
    booking = await db.bookings.get_one_or_none(id = new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.date_from == new_booking.date_from
    # assert (list(booking.model_dump().values())[:-1]) == (list(booking_data.model_dump().values()))

    # Изменить бронь
    new_booking_data = BookingPatch(
        date_from = date(year=2026, month=12, day=25),
        date_to = date(year=2027, month=1, day=5)
    )

    await db.bookings.edit(new_booking_data, exclude_unset=True, id = new_booking.id)
    update_booking = await db.bookings.get_one_or_none()

    assert update_booking
    assert update_booking.id == new_booking.id
    assert update_booking.date_to == date(year=2027, month=1, day=5)

    # Удалить бронь
    await db.bookings.delete(id = update_booking.id)
    booking = await db.bookings.get_one_or_none()
    assert not booking
