from typing import Optional
from sqlalchemy.orm import Session
from app.models.order import Order

class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def update_order(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        if not order:
            raise ValueError("Order not found")
        self.db.delete(order)
        self.db.commit()

    def confirm_order(self, order_id: int) -> Order:
        order = self.get_order(order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = "confirmed"
        self.db.commit()
        self.db.refresh(order)
        return order

    def mark_order_shipped(self, order_id: int) -> Order:
        order = self.get_order(order_id)
        if not order:
            raise ValueError("Order not found")
        order.status = "shipped"
        self.db.commit()
        self.db.refresh(order)
        return order
