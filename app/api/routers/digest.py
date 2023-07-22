from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.depends import Container
from app.api.services import APIService
from app.api.schemas import Digest


router = APIRouter(prefix="/digest")


@router.get("/{user_id}")
@inject
async def get_digest(
    user_id: int, api_service: APIService = Depends(Provide[Container.api_service])
) -> Digest:
    digest = await api_service.get_digest(user_id=user_id)
    return Digest.from_model(digest)
