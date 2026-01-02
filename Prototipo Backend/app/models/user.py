from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True, unique=True)
    nombre = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    activo = Column(Boolean)
    url_icono = Column(String)
