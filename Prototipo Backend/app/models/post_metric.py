from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class PostMetric(Base):
    __tablename__ = "post_metrics"

    id = Column(Integer, primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"))

    metric_name = Column(String)
    period = Column(String)
    value = Column(Integer)
    end_time = Column(DateTime(timezone=True))

    post = relationship("Post", back_populates="metrics")
