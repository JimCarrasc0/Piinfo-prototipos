from fastapi import APIRouter

# =========================================================================
# 1. Importaciones de Rutas
# =========================================================================

# Entidades Principales
from app.api.routes import user
from app.api.routes import login

# --- Router Principal ---
api_router = APIRouter()

# =========================================================================
# 2. Inclusión de Rutas
# =========================================================================

# --- ENTIDADES CORE ---
api_router.include_router(user.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(login.router, prefix="/login", tags=["Autenticación"])