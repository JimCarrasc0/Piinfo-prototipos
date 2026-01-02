# app/db/base.py

from app.db.base_class import Base

# Importa TODOS los modelos para que Alembic los detecte
from app.models.user import User