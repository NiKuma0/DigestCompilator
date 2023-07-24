from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.depends import Container
from app.api.services import APIService
from app.api.schemas import Digest, DigestRequest


router = APIRouter(prefix="/digest")


@router.post("/new")
@inject
async def get_digest(
    request: DigestRequest,
    api_service: APIService = Depends(Provide[Container.api_service]),
) -> Digest:
    digest = await api_service.get_digest(
        user_id=request.user_id,
        unique=request.unique,
        new_than=request.new_than,
        limit=request.limit,
    )
    return Digest.from_model(digest)
