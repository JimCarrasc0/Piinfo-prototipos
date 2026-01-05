from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.services.comment_service import (
    create_comment,
    get_comments,
    update_comment,
    delete_comment
)

router = APIRouter(prefix="/comments", tags=["comments"])


class CommentIn(BaseModel):
    post_id: str
    comment_id: str
    text: str
    sentiment: Optional[str] = "neutral"
    timestamp: datetime


class CommentUpdate(BaseModel):
    text: Optional[str] = None
    sentiment: Optional[str] = None


@router.post("/")
def create(payload: CommentIn):
    create_comment(payload)
    return {"status": "ok"}


@router.get("/", response_model=List[dict])
def list_comments():
    return get_comments()


@router.put("/{comment_id}")
def update(comment_id: int, payload: CommentUpdate):
    updated = update_comment(comment_id, payload)
    if not updated:
        raise HTTPException(404, "Comentario no encontrado")
    return {"status": "ok"}


@router.delete("/{comment_id}")
def delete(comment_id: int):
    deleted = delete_comment(comment_id)
    if not deleted:
        raise HTTPException(404, "Comentario no encontrado, no se pudo borrar")
    return {"status": "ok"}
