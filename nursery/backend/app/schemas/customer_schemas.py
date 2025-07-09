from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    address: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str

    class Config:
        orm_mode = True


class ChangeAddressRequest(BaseModel):
    new_address: str
