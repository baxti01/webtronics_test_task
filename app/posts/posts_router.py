from typing import List

from fastapi import APIRouter, Depends, status, Response

from app.auth.service import get_current_user
from app.posts.serializer import Post, CreatePost, UpdatePost
from app.posts.service import PostsService

router = APIRouter(
    prefix="/posts",
    tags=["Посты"]
)


@router.get('/', response_model=List[Post])
def get_all(
        user_id: int = Depends(get_current_user),
        service: PostsService = Depends()
):
    return service.get_all(user_id)


@router.get("/{post_id}/", response_model=Post)
def get(
        post_id: int,
        user_id: int = Depends(get_current_user),
        service: PostsService = Depends()
):
    return service.get(user_id, post_id)


@router.post("/", response_model=Post)
def create(
        data: CreatePost,
        user_id: int = Depends(get_current_user),
        service: PostsService = Depends()
):
    return service.create(user_id, data)


@router.put("/{post_id}/", response_model=Post)
def update(
        post_id: int,
        data: UpdatePost,
        user_id: int = Depends(get_current_user),
        service: PostsService = Depends()
):
    return service.update(user_id, post_id, data)


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(
        post_id: int,
        user_id: int = Depends(get_current_user),
        service: PostsService = Depends()
):
    service.delete(user_id, post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
