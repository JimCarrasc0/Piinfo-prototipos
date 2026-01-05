from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.post_comment import PostComment, PostCommentCreate
from app import crud

router = APIRouter()


@router.post("/", response_model=PostComment)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_in: PostCommentCreate,
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post_comment.create(db, comment_in)


@router.get("/post/{post_id}", response_model=List[PostComment])
def get_comments_by_post(
    post_id: str,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post_comment.get_by_post(db, post_id)
