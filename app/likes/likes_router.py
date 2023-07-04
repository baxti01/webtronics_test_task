from fastapi import APIRouter, Response, status, Depends

from app.auth.service import get_current_user
from app.likes.service import LikesService

router = APIRouter(
    prefix="/likes",
    tags=["Лайки"]
)


@router.post("/{post_id}/", status_code=status.HTTP_201_CREATED)
def create(
        post_id: int,
        user_id: int = Depends(get_current_user),
        service: LikesService = Depends()
):
    service.create_like(user_id, post_id)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/{post_id}/", status_code=status.HTTP_201_CREATED)
def delete(
        post_id: int,
        user_id: int = Depends(get_current_user),
        service: LikesService = Depends()
):
    service.delete_like(user_id, post_id)
    return Response(status_code=status.HTTP_201_CREATED)
