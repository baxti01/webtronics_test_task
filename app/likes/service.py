from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.config import get_session
from app.database.database_api import DatabaseAPI
from app.database.models import Likes, Posts


class LikesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.database = DatabaseAPI(session)

    def create_like(self, user_id: int, post_id: int) -> None:
        data = {
            "user_id": user_id,
            "post_id": post_id
        }

        post = self.database.get(Posts, id=post_id)
        if post.user_id == user_id:
            return

        try:
            self.database.get(Likes, user_id=user_id, post_id=post_id)
            return
        except Exception:
            self.database.create(Likes, data)
            self._change_likes_count(post)

    def delete_like(self, user_id: int, post_id: int) -> None:
        like = self.database.get(Likes, user_id=user_id, post_id=post_id)
        post = like.post

        self.database.delete(Likes, user_id=user_id, id=like.id)
        self._change_likes_count(post, delete=True)

    def _change_likes_count(self, post: Posts, delete=False):
        if delete:
            count = post.like_count - 1
        else:
            count = post.like_count + 1

        self.database.update(
            Posts,
            {"like_count": count},
            id=post.id
        )
