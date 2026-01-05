from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)  # ID real Meta
    meta_account_id = Column(UUID(as_uuid=True), ForeignKey("meta_accounts.id"))

    message = Column(Text)
    created_time = Column(DateTime(timezone=True))

    meta_account = relationship("MetaAccount", back_populates="posts")
    metrics = relationship("PostMetric", back_populates="post")
    comments = relationship("PostComment", back_populates="post")
    analysis = relationship("PostAnalysis", back_populates="post")
