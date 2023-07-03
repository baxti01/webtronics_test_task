from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.exceptions import invalid_grant_type
from app.auth.serializer import Token, CreateUser
from app.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и регистрация"]
)


@router.post('/sign-up', response_model=Token)
def sing_up(
        data: CreateUser,
        service: AuthService = Depends()
):
    return service.sign_up(user_data=data)


@router.post('/sign-in', response_model=Token)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.sign_in(
        username=form_data.username,
        password=form_data.password
    )


@router.post('/refresh', response_model=Token)
def refresh(
        grant_type: str = Form(regex="refresh_token"),
        refresh_token: str = Form(),
):
    if grant_type == "refresh_token":
        return AuthService.refresh_access_token(token=refresh_token)

    raise invalid_grant_type




