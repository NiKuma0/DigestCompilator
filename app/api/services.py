from app.db.repository import PostRepository, UserRepository, DigestRepository
from app.db import models

from .exceptions import UserDoesNotHaveSubscriptions, UserDoesNotExists


class APIService:
    def __init__(
        self,
        post_repository: PostRepository,
        user_repository: UserRepository,
        digest_repository: DigestRepository,
    ) -> None:
        self._post_repository = post_repository
        self._user_repository = user_repository
        self._digest_repository = digest_repository

    async def _get_user(self, user_id: int) -> models.User:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserDoesNotExists(user_id)
        return user

    async def get_all_posts(self, page=0, page_size=10):
        offset = page * page_size
        return await self._post_repository.get_all(limit=page_size, offset=offset)

    async def get_post(self, post_id: int):
        return await self._post_repository.get_by_id(post_id)

    async def get_digest(self, user_id: int):
        user = await self._get_user(user_id)
        if not user.subscriptions:
            raise UserDoesNotHaveSubscriptions(user_id)
        return await self._digest_repository.create(user)
