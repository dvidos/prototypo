from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from app.modules.customer.customer import Customer
from app.utilities.pagination import Paginator, PaginationInfo

class CustomerService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_customer(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def list_customers(
            self,
            page_num: int = 1,
            page_size: int = 20,
            sort_by: Optional[str] = None,
            sort_order: str = "asc",
            first_name_icontains: Optional[str] = None,
    ) -> Tuple[List[Customer], PaginationInfo]:
        query = self.db.query(Customer)
        if first_name_icontains:
            query = query.filter(Customer.first_name.ilike(f"%{first_name_icontains}%"))

        paginator = Paginator(Customer, page_num=page_num, page_size=page_size, sort_by=sort_by, sort_order=sort_order)
        query, pagination = paginator.apply(query)
        return query.all(), pagination

    def update_customer(self, customer: Customer) -> Customer:
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete_customer(self, customer_id: int) -> None:
        customer = self.get_customer(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        if customer.orders and len(customer.orders) > 0:
            raise ValueError("Cannot delete customer with existing orders")
        self.db.delete(customer)
        self.db.commit()

    def change_address(self, customer_id: int, new_address: str) -> Customer:
        customer = self.get_customer(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        customer.address = new_address
        self.db.commit()
        self.db.refresh(customer)
        return customer
