from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def list(self):
        return self.db.query(Customer).all()

    def create(self, customer: Customer):
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def save(self, customer: Customer):
        self.db.add(customer)  # Optional if already attached
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer_id: int):
        customer = self.get(customer_id)
        if customer:
            self.db.delete(customer)
            self.db.commit()
        return customer
