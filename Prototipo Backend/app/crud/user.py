from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
# Importar la función para verificar contraseñas
from app.core.security import get_password_hash, verify_password 
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# --------------------------------
# --- Funciones CRUD y Lectura ---

def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_active_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Obtiene solo usuarios con activo=True (paginado).
    """
    return db.query(User).filter(User.activo == True).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_obj = User(
        nombre=user.nombre,
        email=user.email,
        password=hashed_password,
        activo=True,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_user(db: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:
    db_obj = get_user(db, user_id)
    if not db_obj: return None
    
    update_data = user_in.model_dump(exclude_unset=True)
    
    # Manejar el hash de la contraseña si se proporciona
    if "password" in update_data and update_data["password"]:
        update_data["password"] = get_password_hash(update_data["password"])
    else:
        update_data.pop("password", None)
        
    for key, value in update_data.items():
        setattr(db_obj, key, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_obj = get_user(db, user_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj

# -----------------------------------------------------------------

## Función de Autenticación 

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    
    if user:
        if verify_password(password, user.password):
            return user 
    
    return None