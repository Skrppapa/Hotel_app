

async def test_get_hotel(ac):
    response = await ac.get(
        "/hotels",
            params = {
                "date_from": "2027-01-01",
                "date_to": "2027-01-15"
            }
    )
    # print(f"{response.json()=}")

    assert response.status_code == 200
