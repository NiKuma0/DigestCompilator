from datetime import date

from sqlalchemy import orm, func


class Base(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    created_at: orm.Mapped[date] = orm.mapped_column(
        server_default=func.current_timestamp()
    )
    updated_at: orm.Mapped[date] = orm.mapped_column(
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id}>"
