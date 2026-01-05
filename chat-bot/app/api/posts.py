from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.post_service import (create_post, get_posts, update_post, delete_post)

router = APIRouter(prefix="/posts", tags=["posts"])

class PostIn(BaseModel):
    post_id: str
    platform: str
    caption: str
    created_at: Optional[str] = None

class PostUpdate(BaseModel):
    caption: Optional[str] = None

@router.post("/")
def create(payload: PostIn):
    create_post(payload)
    return {"status": "ok"}

@router.get("/", response_model=List[dict])
def list_posts():
    return get_posts()

@router.put("/{post_id}")
def update(post_id: str, payload: PostUpdate):
    updated = update_post(post_id, payload)
    if not updated:
        raise HTTPException(404, "Post no encontrado")
    return {"status": "ok"}

@router.delete("/{post_id}")
def delete(post_id: str):
    deleted = delete_post(post_id)
    if not deleted:
        raise HTTPException(404, "Post no encontrado, no se pudo eliminar")
    return {"status": "ok"}
