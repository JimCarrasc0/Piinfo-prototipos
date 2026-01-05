from sqlalchemy.orm import Session
from typing import List

from app.models.post_comment import PostComment
from app.schemas.post_comment import PostCommentCreate


def create(db: Session, obj_in: PostCommentCreate) -> PostComment:
    db_obj = PostComment(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_post(db: Session, post_id: str) -> List[PostComment]:
    return db.query(PostComment).filter(PostComment.post_id == post_id).all()
