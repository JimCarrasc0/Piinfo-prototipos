from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.post import Post, PostCreate
from app import crud

router = APIRouter()


@router.post("/", response_model=Post)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: PostCreate,
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post.create(db, post_in)


@router.get("/{post_id}", response_model=Post)
def get_post(
    post_id: str,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post.get(db, post_id)
