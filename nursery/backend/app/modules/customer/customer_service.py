from typing import Optional, List
from sqlalchemy.orm import Session
from app.modules.customer.customer import Customer

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

    def list_customers(self) -> List[Customer]:
        return self.db.query(Customer).all()

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
