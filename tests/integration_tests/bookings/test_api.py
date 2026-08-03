import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2027-01-01", "2027-01-15", 200),
    (1, "2027-01-02", "2027-01-16", 200),
    (1, "2027-01-03", "2027-01-17", 200),
    (1, "2027-01-04", "2027-01-18", 200),
    (1, "2027-01-05", "2027-01-19", 200),
    (1, "2027-01-06", "2027-01-20", 500),
    (1, "2027-01-25", "2027-01-28", 200),
])

async def test_add_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        db,
        authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "OK"
        assert isinstance(res, dict)
        assert "data" in res
