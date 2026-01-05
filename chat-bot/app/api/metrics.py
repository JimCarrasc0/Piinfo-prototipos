from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.services.metric_service import (create_metric, get_metrics, update_metric, delete_metric)

router = APIRouter(prefix="/metrics", tags=["metrics"])

class MetricIn(BaseModel):
    post_id: str
    metric_name: str
    period: str
    value: float
    end_time: datetime

class MetricUpdate(BaseModel):
    value: float

@router.post("/")
def create(payload: MetricIn):
    create_metric(payload)
    return {"status": "ok"}

@router.get("/", response_model=List[dict])
def list_metrics():
    return get_metrics()

@router.put("/{metric_id}")
def update(metric_id: int, payload: MetricUpdate):
    updated = update_metric(metric_id, payload)
    if not updated:
        raise HTTPException(404, "Métrica no encontrada")
    return {"status": "ok"}

@router.delete("/{metric_id}")
def delete(metric_id: int):
    deleted = delete_metric(metric_id)
    if not deleted:
        raise HTTPException(404, "Métrica no encontrada, no se pudo borrar")
    return {"status": "ok"}
