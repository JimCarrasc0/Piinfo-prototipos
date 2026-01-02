from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    nombre: Optional[str] = None
    activo: Optional[bool] = True
    url_icono: Optional[str] = None

class UserCreate(UserBase):
    password: str # Contraseña requerida al crear

class UserUpdate(BaseModel):
    # Todos los campos opcionales para actualizar
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None 
    activo: Optional[bool] = None
    url_icono: Optional[str] = None

class User(UserBase):
    id_user: int

    class Config:
        from_attributes = True

# Schema auxiliar para manejar la autenticación
class UserInDB(User):
    password: str