from pydantic import BaseModel


class OrderStatusRead(BaseModel):
    value: str
    caption: str

