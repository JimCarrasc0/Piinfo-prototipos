from sqlalchemy.orm import Session
from typing import Optional
from app.models.post import Post
from app.schemas.post import PostCreate


def get(db: Session, id: str) -> Optional[Post]:
    return db.query(Post).filter(Post.id == id).first()


def create(db: Session, obj_in: PostCreate) -> Post:
    db_obj = Post(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
