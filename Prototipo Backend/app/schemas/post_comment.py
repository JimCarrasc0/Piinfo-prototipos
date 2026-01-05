from pydantic import BaseModel
from datetime import datetime


class PostCommentBase(BaseModel):
    message: str | None = None
    created_time: datetime | None = None


class PostCommentCreate(PostCommentBase):
    post_id: str
    comment_id: str


class PostComment(PostCommentBase):
    id: int
    post_id: str
    comment_id: str

    class Config:
        from_attributes = True
