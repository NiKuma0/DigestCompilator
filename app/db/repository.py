from datetime import date
from typing import Generic, TypeVar, Iterable
from abc import ABC

from sqlalchemy import insert, select, ScalarResult, func, desc
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .models import User, Subscription, Post, Digest


Model = TypeVar("Model")


class AbstractRepository(ABC, Generic[Model]):
    __model__: type[Model]

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker

    @classmethod
    @property
    def model(cls) -> type[Model]:
        return cls.__model__

    async def get_by_id(self, _id: int) -> Model | None:
        async with self._sessionmaker() as session:
            return await session.get(self.model, _id)

    async def get_all(self, limit: int = 10, offset: int = 0) -> ScalarResult[Model]:
        async with self._sessionmaker() as session:
            return await session.scalars(select(self.model).limit(limit).offset(offset))

    async def create(self, obj: Model) -> Model:
        async with self._sessionmaker() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj

    async def create_all(self, data: Iterable[dict]) -> ScalarResult[Model]:
        async with self._sessionmaker() as session:
            result = await session.scalars(
                insert(self.model).returning(self.model), data  # type: ignore
            )
            await session.commit()
        return result

    async def update(self, obj: Model) -> Model:
        async with self._sessionmaker() as session:
            return await session.merge(obj)

    async def delete(self, obj: Model):
        async with self._sessionmaker() as session:
            await session.delete(obj)


class UserRepository(AbstractRepository[User]):
    __model__ = User

    async def set_subscriptions(
        self, user: User, subscriptions: Iterable[Subscription]
    ) -> User:
        user.subscriptions.extend(subscriptions)
        async with self._sessionmaker() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user


class SubsRepository(AbstractRepository[Subscription]):
    __model__ = Subscription


class PostRepository(AbstractRepository[Post]):
    __model__ = Post

    async def set_tags(self, post: Post, tags: Iterable[Subscription]) -> Post:
        post.tags.extend(tags)
        async with self._sessionmaker() as session:
            session.add(post)
            await session.commit()
            await session.refresh(post)
        return post


class DigestRepository(AbstractRepository[Digest]):
    __model__ = Digest

    async def get_by_date_and_user_id(self, user_id, created_at: date) -> Digest | None:
        async with self._sessionmaker() as session:
            return await session.scalar(
                select(self.model)
                .where(self.model.created_at == created_at)
                .where(self.model.user_id == user_id)
            )

    async def create(self, user: User) -> Digest:
        """Create a digest for the user"""
        digest = await self.get_by_date_and_user_id(user.id, date.today())
        if digest:
            return digest

        query = (
            select(
                Post,
                (
                    Post.popularity / (func.current_date() - self.model.created_at + 1)
                ).label("relevant"),
            )
            .join(Post.tags)
            .join(Post.digests)
            .where(Subscription.id.in_([tag.id for tag in user.subscriptions]))
            # Unique posts for each digest
            .where(Digest.id.not_in(select(Digest.id).where(Digest.user_id == user.id)))
            .order_by(desc("relevant"))
            .limit(50)
        )
        async with self._sessionmaker() as session:
            posts = await session.scalars(query)
            session.expire_all()
        return await super().create(Digest(posts=posts.all(), user=user))
