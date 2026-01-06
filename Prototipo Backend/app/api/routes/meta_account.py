from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.meta_account import MetaAccount, MetaAccountCreate
from app import crud

router = APIRouter()


@router.get("/", response_model=List[MetaAccount])
def read_my_meta_accounts(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
):
    print("API USER_ID:", current_user.id)
    return crud.meta_account.get_by_user(db, current_user.id)


@router.post("/", response_model=MetaAccount)
def create_meta_account(
    *,
    db: Session = Depends(deps.get_db),
    meta_account_in: MetaAccountCreate,
    current_user = Depends(deps.get_current_active_user),
):
    return crud.meta_account.create(
        db=db,
        user_id=current_user.id,
        obj_in=meta_account_in,
    )
