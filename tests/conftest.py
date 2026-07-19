import pytest
from src.config import settings
from src.database import Base, engine_null_pull
from src.models import *

@pytest.fixture(scope="session", autouse=True)   # scope важный параметр, определяющий как часто будет исполняться фикстура
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
