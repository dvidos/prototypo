from sqlalchemy.orm import Session
from app.models.order import Order, OrderLine

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def list(self):
        return self.db.query(Order).all()

    def create(self, order: Order):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def save(self, customer: Customer):
        self.db.add(customer)  # Optional if already attached
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, order_id: int):
        order = self.get(order_id)
        if order:
            self.db.delete(order)
            self.db.commit()
        return order
