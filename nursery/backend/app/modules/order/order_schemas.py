from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


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



class OrderLineRead(BaseModel):
    sku: str
    description: str
    qty: int
    price: float
    ext_price: float

    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int
    created_at: datetime
    customer_id: int
    total: float
    order_lines: List[OrderLineRead]
    status: str

    model_config = ConfigDict(from_attributes=True)

