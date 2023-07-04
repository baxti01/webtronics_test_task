from pydantic import BaseModel


class BasePost(BaseModel):
    title: str
    content: str


class Post(BasePost):
    id: int
    user_id: int

    like_count: str
    author: str

    class Config:
        orm_mode = True


class CreatePost(BasePost):
    pass


class UpdatePost(BasePost):
    pass
