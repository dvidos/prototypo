from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.modules.customer.customer import Customer
from app.modules.customer.customer_service import CustomerService
from app.modules.customer.customer_schemas import CustomerCreate, CustomerUpdate, CustomerRead, ChangeAddressRequest
from app.dependencies import get_db

router = APIRouter(tags=["customers"])


@router.get("/", response_model=List[CustomerRead])
def list_customers(db: Session = Depends(get_db)) -> List[CustomerRead]:
    service = CustomerService(db)
    customers = service.list_customers()
    return [CustomerRead.from_orm(c) for c in customers]

@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> CustomerRead:
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerRead.from_orm(customer)

@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)) -> CustomerRead:
    service = CustomerService(db)
    created = service.create_customer(Customer(**customer.dict()))
    return CustomerRead.from_orm(created)

@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)) -> CustomerRead:
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for field, value in customer_update.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    updated = service.update_customer(customer)
    return CustomerRead.from_orm(updated)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    service = CustomerService(db)
    service.delete_customer(customer_id)
    return

@router.post("/{customer_id}/actions/change_address", response_model=CustomerRead)
def change_address(customer_id: int, req: ChangeAddressRequest, db: Session = Depends(get_db)) -> CustomerRead:
    service = CustomerService(db)
    customer = service.change_address(customer_id, req.new_address)
    return CustomerRead.from_orm(customer)
