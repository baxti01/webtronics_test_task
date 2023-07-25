import enum

from pydantic import BaseModel


class ReactionType(enum.Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class Reaction(BaseModel):
    type: ReactionType
    post_id: int
