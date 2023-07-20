import asyncio
from datetime import date, timedelta
from typing import Iterable
from random import shuffle, randint

from faker import Faker
from dependency_injector.wiring import inject, Provide

from app.db.repository import UserRepository, SubsRepository, PostRepository
from app.db import models
from app.depends import Container


def get_create_at() -> date:
    return date.today() - timedelta(days=randint(0, 100))


@inject
async def create_users(
    user_repository: UserRepository = Provide[Container.user_repository],
    faker: Faker = Faker(),
    count=100,
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
    count=20,
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
    count=100,
):
    data = []
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
    user_repository: UserRepository = Provide[Container.user_repository],
):
    for user in users:
        shuffle(subs)
        await user_repository.set_subscriptions(user, subs[: randint(1, 20)])


@inject
async def set_tags_posts(
    posts: Iterable[models.Post],
    subs: list[models.Subscription],
    post_repository: PostRepository = Provide[Container.post_repository],
):
    for post in posts:
        shuffle(subs)
        await post_repository.set_tags(post, subs[: randint(1, 5)])


async def main():
    container = Container()
    container.wire([__name__])

    subs = list(await create_subs())
    print("Subscriptions was created")
    users = await create_users()
    print("Users was created")
    posts = await create_posts()
    print("Posts was created")
    await set_tags_posts(posts, subs)
    print("Posts was linked to subs")
    await set_subs_users(users, subs)
    print("User was linked to subs")


if __name__ == "__main__":
    asyncio.run(main())
