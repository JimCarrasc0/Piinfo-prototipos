from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    message: Optional[str]
    created_time: Optional[datetime]


class PostCreate(PostBase):
    id: str
    meta_account_id: UUID


class Post(PostBase):
    id: str
    meta_account_id: UUID

    class Config:
        from_attributes = True
