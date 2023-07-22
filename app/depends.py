from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.settings import get_settings
from app.db import create_engine
from app.db.repository import (
    UserRepository,
    SubsRepository,
    PostRepository,
    DigestRepository,
)
from app.api.services import APIService


class Container(DeclarativeContainer):
    settings = providers.Singleton(get_settings)

    # Database connection
    engine = providers.Singleton(
        create_engine, database_url=settings.provided.database_url
    )
    sessionmaker: providers.Singleton[
        async_sessionmaker[AsyncSession]
    ] = providers.Singleton(async_sessionmaker, bind=engine, expire_on_commit=False)

    # Repositories
    user_repository = providers.Factory(UserRepository, sessionmaker=sessionmaker)
    subs_repository = providers.Factory(SubsRepository, sessionmaker=sessionmaker)
    post_repository = providers.Factory(PostRepository, sessionmaker=sessionmaker)
    digest_repository = providers.Factory(DigestRepository, sessionmaker=sessionmaker)

    # Service
    api_service = providers.Factory(
        APIService,
        post_repository=post_repository,
        user_repository=user_repository,
        digest_repository=digest_repository,
    )
