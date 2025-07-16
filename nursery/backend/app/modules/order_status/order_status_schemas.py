from pydantic import BaseModel


class OrderStatusRead(BaseModel):
    keyword: str
    caption: str

