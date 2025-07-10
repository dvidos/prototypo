from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.modules.order.order import Order
from app.utilities.pagination import Paginator, PaginationInfo

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

    def list_orders(self) -> List[Order]:
        return self.db.query(Order).all()

    def list_orders(
            self,
            page_num: int = 1,
            page_size: int = 20,
            sort_by: Optional[str] = None,
            sort_order: str = "asc",
            status_ieq: Optional[str] = None,
    ) -> Tuple[List[Order], PaginationInfo]:
        query = self.db.query(Order)
        if status_ieq:
            query = query.filter(func.lower(Order.status) == status_ieq.lower())

        paginator = Paginator(Order, page_num=page_num, page_size=page_size, sort_by=sort_by, sort_order=sort_order)
        query, pagination = paginator.apply(query)
        return query.all(), pagination

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
