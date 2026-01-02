# app/api/routes/login.py
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import create_access_token
from app.crud.user import authenticate

router = APIRouter()

@router.post("/access-token", response_model=dict)
def login_access_token(
    db: Session = Depends(deps.get_db),
    # OAuth2PasswordRequestForm espera 'username' (aquí email) y 'password' como Form Data
    form_data: OAuth2PasswordRequestForm = Depends() 
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # 1. Autenticar al usuario
    user = authenticate(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Correo electrónico o contraseña incorrectos"
        )
    if not user.activo:
        # Aquí puedes verificar si el usuario está activo antes de dar el token
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    # 2. Crear y devolver el token
    return {
        "access_token": create_access_token(subject=str(user.id_user)), 
        "token_type": "bearer",
    }