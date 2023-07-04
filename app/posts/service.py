from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.config import get_session
from app.database.database_api import DatabaseAPI
from app.database.models import Posts, Users
from app.posts.serializers import CreatePost, UpdatePost


class PostsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.database = DatabaseAPI(session)

    def get_all(self) -> List[Posts]:
        return self.database.get_all(Posts)

    def get(self, post_id: int) -> Posts:
        return self.database.get(Posts, id=post_id)

    def create(self, user_id: int, data: CreatePost) -> Posts:
        user: Users = self.database.get(Users, id=user_id)

        data_ = data.dict()
        data_["user_id"] = user_id
        data_["author"] = user.username

        return self.database.create(Posts, data_)

    def update(
            self, user_id: int,
            post_id: int,
            data: UpdatePost
    ) -> Posts:
        return self.database.update(
            Posts,
            data.dict(),
            user_id=user_id,
            id=post_id
        )

    def delete(self, user_id: int, post_id: int) -> None:
        self.database.delete(Posts, user_id=user_id, id=post_id)
