from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class OrderCreateLine(BaseModel):
    sku: str
    description: str
    qty: int
    price: float
    ext_price: float

class OrderCreate(BaseModel):
    customer_id: int
    order_lines: List[OrderCreateLine]
    total: float
    status: str




class OrderUpdateLine(BaseModel):
    sku: str
    description: str
    qty: int
    price: float
    ext_price: float

class OrderUpdate(BaseModel):
    order_lines: Optional[List[OrderUpdateLine]] = None
    total: Optional[float] = None
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

