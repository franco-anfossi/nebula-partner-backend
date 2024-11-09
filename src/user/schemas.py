from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    id_auth0: Optional[str] = None


class UserUpdate(BaseModel):
    # Campos de tu modelo local
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

    # Campos que se sincronizan con Auth0
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id_auth0: str

    class Config:
        orm_mode = True
