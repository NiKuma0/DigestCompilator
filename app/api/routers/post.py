from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.api.schemas import Post, Paginator
from app.api.exceptions import PostNotFoundError
from app.api.services import APIService
from app.depends import Container


router = APIRouter(prefix="/posts")


@router.get("/all")
@inject
async def get_posts(
    page: int = 0,
    page_size: int = 10,
    api_service: APIService = Depends(Provide[Container.api_service]),
) -> Paginator[list[Post]]:
    posts = await api_service.get_all_posts(page=page, page_size=page_size)
    result: list[Post] = []
    for post in posts:
        result.append(Post.from_model(post))
    return Paginator(data=result, page=page)


@router.get("/{post_id}")
@inject
async def get_post(
    post_id: int = 0,
    api_service: APIService = Depends(Provide[Container.api_service]),
) -> Post:
    post = await api_service.get_post(post_id)
    if not post:
        raise PostNotFoundError(post_id)
    return Post.from_model(post)
