from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.meta_account import MetaAccount
from app.schemas.meta_account import MetaAccountCreate


def get_by_user(db: Session, user_id: UUID) -> List[MetaAccount]:
    return db.query(MetaAccount).filter(MetaAccount.user_id == user_id).all()


def get(db: Session, id: UUID) -> Optional[MetaAccount]:
    return db.query(MetaAccount).filter(MetaAccount.id == id).first()


def create(db: Session, user_id: UUID, obj_in: MetaAccountCreate) -> MetaAccount:
    db_obj = MetaAccount(
        user_id=user_id,
        page_id=obj_in.page_id,
        page_name=obj_in.page_name,
        access_token=obj_in.access_token,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def create_or_update(
    db: Session,
    user_id: int,
    page_id: str,
    page_name: str,
    access_token: str,
):
    obj = (
        db.query(MetaAccount)
        .filter(MetaAccount.page_id == page_id)
        .first()
    )

    if obj:
        obj.access_token = access_token
    else:
        obj = MetaAccount(
            user_id=user_id,
            page_id=page_id,
            page_name=page_name,
            access_token=access_token,
        )
        db.add(obj)

    db.commit()
    db.refresh(obj)
    return obj