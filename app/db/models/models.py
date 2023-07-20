from sqlalchemy import orm, ForeignKey, String, Text

from .base import Base


class User(Base):
    __tablename__ = "users"

    name: orm.Mapped[str]

    digests: orm.Mapped[list["Digest"]] = orm.relationship(back_populates="user")
    subscriptions: orm.Mapped[list["Subscription"]] = orm.relationship(
        secondary="user_subs_link",
        back_populates="subscribers",
        lazy="selectin",
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    name: orm.Mapped[str]

    subscribers: orm.Mapped[list["User"]] = orm.relationship(
        secondary="user_subs_link", back_populates="subscriptions"
    )
    posts: orm.Mapped[list["Post"]] = orm.relationship(
        secondary="post_subs_link", back_populates="tags"
    )


class Post(Base):
    __tablename__ = "posts"

    title: orm.Mapped[str] = orm.mapped_column(String(256))
    content: orm.Mapped[str] = orm.mapped_column(Text)
    popularity: orm.Mapped[int]

    tags: orm.Mapped[list["Subscription"]] = orm.relationship(
        secondary="post_subs_link",
        back_populates="posts",
        lazy="selectin",
    )
    digests: orm.Mapped[list["Digest"]] = orm.relationship(
        secondary="post_digest_link", back_populates="posts"
    )


class Digest(Base):
    __tablename__ = "digests"

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id"))
    user: orm.Mapped["User"] = orm.relationship(back_populates="digests")

    posts: orm.Mapped[list["Post"]] = orm.relationship(
        secondary="post_digest_link",
        back_populates="digests",
        lazy="selectin",
    )
