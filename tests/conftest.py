import json
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.config import settings
from src.database import Base, engine_null_pull, engine, async_session_maker_null_pull
from src.main import app
from src.models import *
from httpx import AsyncClient, ASGITransport
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)  # scope важный параметр, определяющий как часто будет исполняться фикстура
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Добавление тестовых данных из файлов
    with open('tests/mock_hotels.json', 'r', encoding="utf-8") as hotel_file:
        hotels_data = json.load(hotel_file)
    with open('tests/mock_rooms.json', 'r', encoding="utf-8") as room_file:
        rooms_data = json.load(room_file)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pull) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

# Переиспользуемый объект AsyncClient для тестирования API
@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@mail.com",
            "password": "12345"
        }
    )





