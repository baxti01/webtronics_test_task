from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.auth.exceptions import invalid_credentials, incorrect_data
from app.auth.serializer import CreateUser, Token
from app.database import models
from app.database.config import get_session
from app.database.database_api import DatabaseAPI
from app.settings import settings


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.database = DatabaseAPI(session)

    def sign_up(self, user_data: CreateUser) -> Token:
        password_hash = self.hash_password(user_data.password)
        data = user_data.dict(exclude={"password"})
        data['password_hash'] = password_hash

        user = self.database.create(table=models.Users, data=data)

        return self.create_token_pair(user.id)

    def sign_in(self, username: str, password: str) -> Token:
        user = self.database.get(
            table=models.Users,
            exception=incorrect_data,
            username=username
        )

        if not self.verify_password(password, user.password_hash):
            raise incorrect_data

        return self.create_token_pair(user.id)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> int:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.jwt_secret,
                algorithms=settings.jwt_algorithm
            )
        except JWTError:
            raise invalid_credentials

        user_id = payload.get("sub", None)

        return int(user_id)

    @classmethod
    def create_token(cls, user_id: int, expired: int) -> str:
        date = datetime.utcnow()
        payload = {
            "iat": date,
            "nbf": date,
            "exp": date + timedelta(minutes=expired),
            "sub": str(user_id)
        }

        token = jwt.encode(
            payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,

        )

        return token

    @classmethod
    def create_token_pair(cls, user_id: int):
        access_token = cls.create_token(user_id, expired=settings.jwt_access_token_expire)
        refresh_token = cls.create_token(user_id, expired=settings.jwt_refresh_token_expire)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @classmethod
    def refresh_access_token(cls, token: str) -> Token:
        user_id = cls.verify_token(token)
        access_token = cls.create_token(user_id, expired=settings.jwt_access_token_expire)

        return Token(access_token=access_token)
