from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    address: str


class CustomerUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    address: str

    model_config = ConfigDict(from_attributes=True)


class ChangeAddressRequest(BaseModel):
    new_address: str


class CustomerBulkRequest(BaseModel):
    ids: List[int]


