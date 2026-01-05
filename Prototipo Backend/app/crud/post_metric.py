from sqlalchemy.orm import Session
from typing import List

from app.models.post_metric import PostMetric
from app.schemas.post_metric import PostMetricCreate


def create(db: Session, obj_in: PostMetricCreate) -> PostMetric:
    db_obj = PostMetric(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_post(db: Session, post_id: str) -> List[PostMetric]:
    return db.query(PostMetric).filter(PostMetric.post_id == post_id).all()
