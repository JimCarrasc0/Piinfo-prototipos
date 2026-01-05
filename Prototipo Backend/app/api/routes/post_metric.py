from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.post_metric import PostMetric, PostMetricCreate
from app import crud

router = APIRouter()


@router.post("/", response_model=PostMetric)
def create_metric(
    *,
    db: Session = Depends(deps.get_db),
    metric_in: PostMetricCreate,
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post_metric.create(db, metric_in)


@router.get("/post/{post_id}", response_model=List[PostMetric])
def get_metrics_by_post(
    post_id: str,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post_metric.get_by_post(db, post_id)
