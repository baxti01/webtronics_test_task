from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseUser):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
