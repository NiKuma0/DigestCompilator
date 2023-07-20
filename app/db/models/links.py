from sqlalchemy import orm, ForeignKey

from .base import Base


class PostSubsLink(Base):
    __tablename__ = "post_subs_link"

    post_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("posts.id"))
    subs_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("subscriptions.id"))


class UserSubsLink(Base):
    __tablename__ = "user_subs_link"

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id"))
    subs_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("subscriptions.id"))


class PostDigestLink(Base):
    __tablename__ = "post_digest_link"

    post_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("posts.id"))
    digest_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("digests.id"))
