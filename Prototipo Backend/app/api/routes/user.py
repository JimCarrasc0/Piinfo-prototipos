# app/api/routes/user.py

from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps 
from app.schemas.user import User, UserCreate, UserUpdate 
from app.models.user import User as UserModel 

router = APIRouter()

# --- GET Todos los Usuarios (Paginado) ---
@router.get("/", response_model=List[User]) 
def read_users(
    db: Session = Depends(deps.get_db),
    # APLICAR SEGURIDAD: Solo usuarios autenticados y activos pueden listar usuarios
    current_user: UserModel = Depends(deps.get_current_active_user), 
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Obtener todos los usuarios (incluidos inactivos). (Requiere autenticación)
    """
    # [NOTA: Aquí iría la verificación de rol si solo los administradores deben listar]
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users
    
# --- GET Usuarios Activos (Paginado) ---
@router.get("/activos", response_model=List[User]) 
def read_active_users(
    db: Session = Depends(deps.get_db),
    # APLICAR SEGURIDAD: Solo usuarios autenticados y activos pueden listar usuarios
    current_user: UserModel = Depends(deps.get_current_active_user), 
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Obtener solo usuarios activos (activo=True). (Requiere autenticación)
    """
    users = crud.user.get_active_users(db, skip=skip, limit=limit)
    return users

# --- POST (Creación de Usuario / Registro) ---
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate, # Usamos UserCreate importado
) -> Any:
    # ... (Sin cambios)
    """
    Crear un nuevo usuario. (Ruta abierta por defecto para registro)
    """
    user = crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    user = crud.user.create_user(db, user=user_in)
    return user

# --- PUT (Actualización de Usuario) ---
@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate, # Usamos UserUpdate importado
    # APLICAR SEGURIDAD: Solo usuarios autenticados y activos pueden actualizar
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    # ... (Sin cambios)
    """
    Actualizar un usuario. (Requiere autenticación)
    """
    # [NOTA: Implementar aquí la lógica de que el usuario solo puede actualizarse a sí mismo o si es admin]
    user = crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    if user_in.email and user_in.email != user.email:
        existing_user = crud.user.get_user_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo email ya está en uso por otro usuario"
            )
            
    user = crud.user.update_user(db, user_id=user_id, user_in=user_in)
    return user
# --- Obtener Usuario Actual (users/me) ---
@router.get("/me", response_model=User)
def read_user_me(
    # Usamos get_current_active_user para asegurar que el usuario esté logueado Y activo
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obtener la información del usuario autenticado actualmente (requiere token válido).
    """
    # La dependencia 'get_current_active_user' ya realiza la decodificación,
    # la búsqueda en la DB y la verificación de actividad.
    # Solo devolvemos el objeto User.
    return current_user
# --- GET por ID (Lectura de Usuario) ---
@router.get("/{user_id}", response_model=User)
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    # APLICAR SEGURIDAD: Solo usuarios autenticados y activos pueden leer
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    # ... (Sin cambios)
    """
    Obtener un usuario por ID. (Requiere autenticación)
    """
    # [NOTA: Implementar aquí la lógica de que el usuario solo puede leerse a sí mismo o si es admin]
    user = crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# --- DELETE (Eliminación de Usuario) ---
@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    # APLICAR SEGURIDAD: Solo usuarios autenticados y activos pueden eliminar
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    # ... (Sin cambios)
    """
    Eliminar un usuario por ID. (Requiere autenticación y se recomienda solo para administradores)
    """
    # [NOTA: Implementar aquí la verificación de rol de administrador]
    user = crud.user.delete_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

