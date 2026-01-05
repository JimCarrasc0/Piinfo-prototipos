from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nombre: Optional[str] = None
    activo: Optional[bool] = True
    
class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    # Todos los campos opcionales para actualizar
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None 
    activo: Optional[bool] = None

class User(UserBase):
    id: UUID
    email: EmailStr
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Schema auxiliar para manejar la autenticación
class UserInDB(User):
    password: str