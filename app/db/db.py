from sqlalchemy.ext.asyncio import create_async_engine


def create_engine(database_url: str):
    return create_async_engine(url=database_url)
