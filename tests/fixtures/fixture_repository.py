import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import UserRepository


@pytest.fixture
async def user_repository(session: AsyncSession):
    yield UserRepository(session)
