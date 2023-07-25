from fastapi import APIRouter, Response, status, Depends

from app.auth.service import get_current_user
from app.likes.serializers import Reaction
from app.likes.service import ReactionsService

router = APIRouter(
    prefix="/likes",
    tags=["Лайки"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
        reaction_data: Reaction,
        user_id: int = Depends(get_current_user),
        service: ReactionsService = Depends()
):
    service.create_reaction(user_id, reaction_data)
    return {"detail": "Reaction created"}


@router.put("/")
def update(
        reaction_data: Reaction,
        user_id: int = Depends(get_current_user),
        service: ReactionsService = Depends()
):
    service.update_reaction(user_id, reaction_data)
    return {"detail": "Reaction updated"}


@router.delete("/")
def delete(
        reaction_data: Reaction,
        user_id: int = Depends(get_current_user),
        service: ReactionsService = Depends()
):
    service.delete_reaction(user_id, reaction_data)
    return {"detail": "Reaction deleted"}
