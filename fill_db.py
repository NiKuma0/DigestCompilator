from datetime import date, timedelta
import asyncio
from typing import Iterable, Any
from random import randint, choices

from faker import Faker
from dependency_injector.wiring import inject, Provide
from sqlalchemy import insert, delete, select, func
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.db.repository import UserRepository, SubsRepository, PostRepository
from app.db.models import links
from app.db import models
from app.depends import Container


db_date: date


@inject
async def get_current_date(
    sessionmaker: async_sessionmaker[AsyncSession] = Provide[Container.sessionmaker],
) -> date:
    async with sessionmaker() as session:
        result = await session.execute(select(func.current_date()))
    return result.scalar_one()


def get_create_at():
    return db_date - timedelta(days=randint(0, 100))


@inject
async def clear_tables(
    sessionmaker: async_sessionmaker[AsyncSession] = Provide[Container.sessionmaker],
):
    async with sessionmaker() as session:
        await session.execute(delete(links.UserSubsLink))
        await session.execute(delete(links.PostSubsLink))
        await session.execute(delete(links.PostDigestLink))
        await session.execute(delete(models.Digest))
        await session.execute(delete(models.Post))
        await session.execute(delete(models.Subscription))
        await session.execute(delete(models.User))
        await session.commit()


@inject
async def create_users(
    user_repository: UserRepository = Provide[Container.user_repository],
    faker: Faker = Faker(),
    count: int = 100,
):
    return await user_repository.create_all(
        [
            dict(
                name=faker.user_name(),
                created_at=(created_at := get_create_at()),
                updated_at=created_at,
            )
            for _ in range(count)
        ]
    )


@inject
async def create_subs(
    subs_repository: SubsRepository = Provide[Container.subs_repository],
    faker: Faker = Faker(),
    count: int = 20,
):
    return await subs_repository.create_all(
        [
            dict(
                name=faker.slug(),
                created_at=(created_at := get_create_at()),
                updated_at=created_at,
            )
            for _ in range(count)
        ]
    )


@inject
async def create_posts(
    post_repository: PostRepository = Provide[Container.post_repository],
    faker: Faker = Faker(),
    count: int = 100,
):
    data: list[dict[str, Any]] = []
    for _ in range(count):
        data.append(
            dict(
                title=faker.text(256),
                content=faker.text(),
                popularity=randint(0, 50) + randint(0, 50),
                created_at=(created_at := get_create_at()),
                updated_at=created_at,
            )
        )
    return await post_repository.create_all(data)


@inject
async def set_subs_users(
    users: Iterable[models.User],
    subs: list[models.Subscription],
    sessionmaker: async_sessionmaker[AsyncSession] = Provide[Container.sessionmaker],
):
    user_sub_links = []
    for user in users:
        for sub in choices(subs, k=randint(1, 5)):
            user_sub_links.append(dict(user_id=user.id, subs_id=sub.id))
    async with sessionmaker() as session:
        await session.execute(insert(links.UserSubsLink), user_sub_links)
        await session.commit()


@inject
async def set_tags_posts(
    posts: Iterable[models.Post],
    subs: list[models.Subscription],
    sessionmaker: async_sessionmaker[AsyncSession] = Provide[Container.sessionmaker],
):
    post_sub_links = []
    for post in posts:
        for sub in choices(subs, k=randint(1, 5)):
            post_sub_links.append(dict(post_id=post.id, subs_id=sub.id))
    async with sessionmaker() as session:
        await session.execute(insert(links.PostSubsLink), post_sub_links)
        await session.commit()


async def main():
    container = Container()
    container.wire([__name__])

    global db_date

    db_date = await get_current_date()

    await clear_tables()
    print("Tables was cleared")
    subs = list(await create_subs(count=1_000))
    print("Subscriptions was created")
    users = await create_users(count=1_000)
    print("Users was created")
    posts = await create_posts(count=10_000)
    print("Posts was created")
    await set_tags_posts(posts, subs)
    print("Posts was linked to subs")
    await set_subs_users(users, subs)
    print("User was linked to subs")


if __name__ == "__main__":
    asyncio.run(main())
