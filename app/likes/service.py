from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.config import get_session
from app.database.database_api import DatabaseAPI
from app.database.models import Likes, Posts
from app.likes.excaptions import owner_error, already_created
from app.likes.serializers import Reaction, ReactionType
from app.posts.serializers import UpdatePost
from app.posts.service import PostsService


class ReactionService:
    def __init__(self, session: Session = Depends(get_session)):
        self.database = DatabaseAPI(session)

    def create(self, user_id: int, like_type: Reaction) -> None:
        data = {
            "user_id": user_id,
            "post_id": like_type.post_id,
            "type": like_type.type
        }

        post = self.database.get(Posts, id=like_type.post_id)

        if post.user_id == user_id:
            raise owner_error

        try:
            self.database.get(Likes, user_id=user_id, post_id=like_type.post_id)
            raise already_created
        except Exception:
            self.database.create(Likes, data)

            if like_type.type == ReactionType.LIKE:
                like_count = post.like_count + 1
                self.database.update(Posts, {"like_count": like_count}, id=post.id)
            else:
                dislike_count = post.dislike_count + 1
                self.database.update(Posts, {"dislike_count": dislike_count}, id=post.id)

    def update(self, user_id: int, like_type: Reaction):
        like = self.database.get(Likes, user_id=user_id, post_id=like_type.post_id)
        post = like.post
        data = {}

        if like_type.type == like.type:
            raise already_created

        if like_type.type == ReactionType.LIKE:
            data['like_count'] = post.like_count + 1
            data['dislike_count'] = post.dislike_count - 1
        if like_type.type == ReactionType.DISLIKE:
            data['like_count'] = post.like_count - 1
            data['dislike_count'] = post.dislike_count + 1

        self.database.update(Posts, data, id=like_type.post_id)

    def delete(self, user_id: int, like_type: Reaction) -> None:
        like = self.database.get(Likes, user_id=user_id, post_id=like_type.post_id)
        post = like.post

        self.database.delete(Likes, user_id=user_id, id=like.id)
        self._change_likes_count(post, like_type=like_type.type, delete=True)

    def change(self, like_type: Reaction):
        post = self.database.get(Posts, id=like_type.post_id)
        if like_type.type == ReactionType.LIKE:
            pass
        if like_type.type == ReactionType.DISLIKE:
            pass

    def _change_likes_count(
            self,
            post: Posts,
            like_type=ReactionType.LIKE,
            delete=False
    ):
        if like_type == ReactionType.DISLIKE:
            count = self._change_count(post.dislike_count, delete)

            self.database.update(
                Posts,
                {"dislike_count": count},
                id=post.id
            )
        else:
            count = self._change_count(post.like_count, delete)

            self.database.update(
                Posts,
                {"like_count": count},
                id=post.id
            )

    def _change_count(self, value, delete=False):
        if delete:
            count = value - 1
        else:
            count = value + 1

        return count


class ReactionsService:

    def __init__(
            self,
            session: Session = Depends(get_session)
    ):
        self.session = session

    def _get_reaction(
            self,
            user_id: int,
            post_id: int,
            exception: bool = False
    ) -> Likes:
        reaction = (
            self.session.query(Likes)
            .filter_by(
                post_id=post_id,
                user_id=user_id
            )
            .first()
        )

        if exception and not reaction:
            raise HTTPException(
                detail="Reaction not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return reaction

    def create_reaction(
            self,
            user_id: int,
            reaction: Reaction,
    ) -> None:
        post_service = PostsService(session=self.session)
        post = post_service.get(reaction.post_id)

        if post.user_id == user_id:
            raise HTTPException(
                detail="You can't like or dislike your posts",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        old_reaction = self._get_reaction(user_id, reaction.post_id)
        if old_reaction:
            raise HTTPException(
                detail="The reaction has already been created,"
                       " try to update it.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        new_reaction = Likes(
            type=reaction.type,
            post_id=reaction.post_id,
            user_id=user_id
        )

        reaction_count_attr = f"{reaction.type.value}_count"
        count = getattr(post, reaction_count_attr)
        setattr(post, "like_count", count + 1)

        self.session.add(new_reaction)
        self.session.commit()
        self.session.refresh(new_reaction)

    def update_reaction(
            self,
            user_id: int,
            reaction: Reaction,

    ) -> None:
        old_reaction = self._get_reaction(
            user_id=user_id,
            post_id=reaction.post_id,
            exception=True
        )

        if old_reaction.type == reaction.type:
            raise HTTPException(
                detail="Such a reaction has already been established",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        old_reaction.type = reaction.type
        self._update_post_reaction(
            post=old_reaction.post,
            reaction=reaction
        )

        self.session.commit()

    def delete_reaction(
            self,
            user_id: int,
            reaction: Reaction,

    ) -> None:
        old_reaction = self._get_reaction(
            user_id=user_id,
            post_id=reaction.post_id,
            exception=True
        )
        if old_reaction.type != reaction.type:
            raise HTTPException(
                detail="Reaction not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        self._update_post_reaction(
            post=old_reaction.post,
            reaction=reaction,
            delete=True
        )

        self.session.delete(old_reaction)
        self.session.commit()

    def _update_post_reaction(
            self,
            post: Posts,
            reaction: Reaction,
            delete: bool = False
    ) -> None:
        if reaction.type == ReactionType.LIKE:
            if delete:
                post.like_count -= 1
            else:
                post.like_count += 1

            if post.dislike_count and not delete:
                post.dislike_count -= 1
        else:
            if delete:
                post.dislike_count -= 1
            else:
                post.dislike_count += 1

            if post.like_count and not delete:
                post.like_count -= 1
