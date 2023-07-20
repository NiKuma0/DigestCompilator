from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__name__).parent
TESTING = True


class Settings(BaseSettings):
    # Postgres Settings
    POSTGRES_DB: str = "app"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


def get_settings() -> Settings:
    if TESTING and (env_file := BASE_DIR / ".env").exists():
        return Settings(_env_file=env_file)  # type: ignore
    return Settings()  # type: ignore
