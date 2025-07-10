from pydantic import BaseModel
from typing import List, Optional


class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItem]
    total_amount: float
    status: str


class OrderUpdate(BaseModel):
    items: Optional[List[OrderItem]] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None


class OrderRead(BaseModel):
    id: int
    customer_id: int
    items: List[OrderItem]
    total_amount: float
    status: str

    class Config:
        orm_mode = True

