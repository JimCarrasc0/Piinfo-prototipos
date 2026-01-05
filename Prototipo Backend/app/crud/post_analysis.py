from sqlalchemy.orm import Session
from typing import List

from app.models.post_analysis import PostAnalysis
from app.schemas.post_analysis import PostAnalysisCreate


def create(db: Session, obj_in: PostAnalysisCreate) -> PostAnalysis:
    db_obj = PostAnalysis(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_post(db: Session, post_id: str) -> List[PostAnalysis]:
    return db.query(PostAnalysis).filter(PostAnalysis.post_id == post_id).all()
