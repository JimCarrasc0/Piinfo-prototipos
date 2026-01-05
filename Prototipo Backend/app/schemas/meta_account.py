from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class MetaAccountBase(BaseModel):
    page_id: str
    page_name: Optional[str] = None


class MetaAccountCreate(MetaAccountBase):
    access_token: str


class MetaAccount(MetaAccountBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
