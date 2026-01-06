from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base_class import Base


class MetaAccount(Base):
    __tablename__ = "meta_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    page_id = Column(String, nullable=False)
    page_name = Column(String)
    access_token = Column(Text, nullable=False)

    instagram_account_id = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    user = relationship(
        "User",
        back_populates="meta_accounts"
    )

    posts = relationship(
        "Post",
        back_populates="meta_account",
        cascade="all, delete-orphan"
    )
