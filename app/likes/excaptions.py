from fastapi import HTTPException, status

already_created = HTTPException(
    detail="Реакция уже создана",
    status_code=status.HTTP_400_BAD_REQUEST
)

owner_error = HTTPException(
    detail="Вы не можете лайкать свои посты",
    status_code=status.HTTP_400_BAD_REQUEST
)
