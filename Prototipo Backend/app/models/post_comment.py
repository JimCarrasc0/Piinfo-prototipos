from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"))

    comment_id = Column(String, unique=True)
    message = Column(Text)
    created_time = Column(DateTime(timezone=True))

    post = relationship("Post", back_populates="comments")
