import uvicorn
from fastapi import FastAPI

from app.depends import Container

from app.api.routers import api_router


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api")

    @app.on_event("startup")
    async def _():
        container = Container()
        container.wire(packages=("app",))

    return app


if __name__ == "__main__":
    uvicorn.run(init_app())
