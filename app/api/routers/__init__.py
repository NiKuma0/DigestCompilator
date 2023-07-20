from fastapi import APIRouter

from .healthchek import router as healthcheck_router
from .post import router as post_router
from .digest import router as digest_router


api_router = APIRouter()
api_router.include_router(healthcheck_router, tags=["healthcheck"])
api_router.include_router(post_router, tags=["Posts"])
api_router.include_router(digest_router, tags=["Digest"])


__all__ = (
    "healthcheck_router",
    "post_router",
    "digest_router",
    "api_router",
)
