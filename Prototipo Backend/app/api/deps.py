from typing import Generator, Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from uuid import UUID
from app.db.session import SessionLocal
from app import crud
from app.models.user import User 
from app.core.config import SECRET_KEY, ALGORITHM 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")

class TokenData(BaseModel):
    # 'sub' (subject) debe ser el ID del usuario (str o int)
    sub: Optional[str] = None 


# ==============================================================================
# 1. DEPENDENCIA: Sesión de Base de Datos
# ==============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Proporciona una sesión de DB por solicitud y asegura su cierre (try/finally).
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ==============================================================================
# 2. DEPENDENCIA: Obtener Usuario a partir del Token (Decodificación)
# ==============================================================================

def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """
    Decodifica el token JWT y busca al usuario por su ID (sub) en la DB.
    """
    try:
        # Decodificar el Token
        payload = jwt.decode(
            token, 
            str(SECRET_KEY), 
            algorithms=[ALGORITHM]
        )
        # user_id_str será el valor de 'sub' (debería ser el ID numérico como string)
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación inválido (sin ID de usuario)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Asignamos el sub a Pydantic para validación (aunque ya lo validamos como not None)
        token_data = TokenData(sub=user_id_str)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas (token expirado o corrupto)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id_value = token_data.sub
    
    try:
        user_id_uuid = UUID(user_id_value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID de usuario en el token no es un UUID válido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Búsqueda del usuario por el ID numérico
    user = crud.user.get_user(db, user_id=user_id_uuid)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    
    return user

# ==============================================================================
# 3. DEPENDENCIA: Obtener Usuario Activo
# ==============================================================================

def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Verifica que el usuario obtenido del token esté activo (activo=True).
    """
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    return current_user