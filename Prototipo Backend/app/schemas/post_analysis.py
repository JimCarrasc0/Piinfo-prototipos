from pydantic import BaseModel
from typing import Any
from datetime import datetime


class PostAnalysisBase(BaseModel):
    analysis_type: str
    result: Any


class PostAnalysisCreate(PostAnalysisBase):
    post_id: str


class PostAnalysis(PostAnalysisBase):
    id: int
    post_id: str
    created_at: datetime

    class Config:
        from_attributes = True
