import uvicorn
from fastapi import FastAPI

from app.depends import Container

from app.api.routers import api_router


def init_app(container_factory: type[Container] = Container) -> FastAPI:
    container = container_factory()
    container.wire(packages=("app",))

    app = FastAPI()
    app.include_router(api_router, prefix="/api")

    return app


if __name__ == "__main__":
    uvicorn.run(init_app())  # type: ignore
