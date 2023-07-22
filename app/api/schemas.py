from datetime import date
from typing import TypeVar, Generic

from pydantic import BaseModel

from app.db import models

Schema = TypeVar("Schema")


class Paginator(BaseModel, Generic[Schema]):
    data: Schema
    page: int


class Post(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    popularity: int
    publication_date: date

    @classmethod
    def from_model(cls, post: models.Post):
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            popularity=post.popularity,
            publication_date=post.created_at,
            tags=[tag.name for tag in post.tags],
        )


class Digest(BaseModel):
    id: int
    user_id: int
    posts: list["Post"]

    @classmethod
    def from_model(cls, digest: models.Digest):
        return cls(
            id=digest.id,
            user_id=digest.user_id,
            posts=[Post.from_model(post) for post in digest.posts],
        )
