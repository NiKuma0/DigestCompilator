import pytest

from sqlalchemy.ext.asyncio import AsyncEngine

from app.settings import Settings
from app.db import create_engine, get_session


@pytest.fixture
def settings():
    return Settings(
        POSTGRES_USER="postgres",
        POSTGRES_PASSWORD="postgres",
    )


@pytest.fixture
def engine(settings: Settings):
    return create_engine(settings.database_url)


@pytest.fixture
async def session(engine: AsyncEngine):
    yield await anext(get_session(engine))
