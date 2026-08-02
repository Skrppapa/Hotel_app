from src.repositories.bookings import BookingsRepository


async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    print(room_id)
    await BookingsRepository.add_booking(room = room_id)
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2027-01-01",
            "date_to": "2027-01-15",
        }
    )

    assert response.status_code == 200

    res = response.json()
    assert res["status"] == "OK"
    assert isinstance(res, dict)
    assert "data" in res
