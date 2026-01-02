# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

from passlib.context import CryptContext
from jose import jwt

# 💡 CORRECCIÓN: Importamos las constantes necesarias directamente de config.py
from app.core.config import (
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES
) 

# 1. Configuración de Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 2. Funciones de Hashing de Contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña plana coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Protección defensiva (bcrypt limit)
    password = password[:72]
    return pwd_context.hash(password)




# 3. Funciones de JWT (Tokens)
def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Crea un token de acceso JWT."""
    
    # Obtener el tiempo de expiración
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Usamos la constante ACCESS_TOKEN_EXPIRE_MINUTES
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # El 'sub' (subject) es el ID del usuario
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Usamos las constantes SECRET_KEY y ALGORITHM
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt