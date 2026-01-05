from pydantic import BaseModel
from datetime import datetime


class PostMetricCreate(BaseModel):
    post_id: str
    metric_name: str
    period: str
    value: int
    end_time: datetime


class PostMetric(PostMetricCreate):
    id: int

    class Config:
        from_attributes = True
