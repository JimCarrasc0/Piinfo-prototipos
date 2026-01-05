from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.post_analysis import PostAnalysis, PostAnalysisCreate
from app import crud

router = APIRouter()


@router.post("/", response_model=PostAnalysis)
def create_analysis(
    *,
    db: Session = Depends(deps.get_db),
    analysis_in: PostAnalysisCreate,
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post_analysis.create(db, analysis_in)


@router.get("/post/{post_id}", response_model=List[PostAnalysis])
def get_analysis_by_post(
    post_id: str,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
):
    return crud.post_analysis.get_by_post(db, post_id)
