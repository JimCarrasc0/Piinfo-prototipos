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
    user_id: UUID,
    page_id: str,
    page_name: str,
    access_token: str,
    instagram_account_id: str,
):
    print("DB URL:", db.bind.url)

    obj = (
        db.query(MetaAccount)
        .filter(
            MetaAccount.user_id == user_id,
            MetaAccount.page_id == page_id,
        )
        .first()
    )

    if not obj:
        obj = MetaAccount(
            user_id=user_id,
            page_id=page_id,
            page_name=page_name,
            access_token=access_token,
            instagram_account_id=instagram_account_id,
        )
        db.add(obj)
    else:
        obj.page_name = page_name
        obj.access_token = access_token
        obj.instagram_account_id = instagram_account_id

    db.commit()          # 👈 IMPRESCINDIBLE
    db.refresh(obj)
    print("CREATED:", obj.id)
    return obj
