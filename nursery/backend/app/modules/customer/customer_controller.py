from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.customer.customer import Customer
from app.modules.customer.customer_service import CustomerService
from app.modules.customer.customer_schemas import (CustomerCreate, CustomerUpdate, CustomerRead, ChangeAddressRequest,
                                                   CustomerBulkRequest)
from app.dependencies import get_db
from app.utilities.pagination import Paginator, Paginated
from app.utilities.bulk import BulkResponse

router = APIRouter(tags=["customers"])


@router.get("/", response_model=Paginated[CustomerRead])
def list_customers(
        db: Session = Depends(get_db),
        page_num: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        sort_by: Optional[str] = Query(None),
        sort_order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
        first_name__icontains: Optional[str] = None,
):
    service = CustomerService(db)
    [customers, pagination] = service.list_customers(
        page_num=page_num,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        first_name_icontains=first_name__icontains
    )
    return Paginated[CustomerRead](pagination=pagination, results=customers)


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

@router.post("/bulk/delete", response_model=BulkResponse)
def bulk_delete(req: CustomerBulkRequest, db: Session = Depends(get_db)):
    service = CustomerService(db)
    # the process should be performed in bulk in the service as well
    # it's up to the service to validate in bulk or in each individual entity
    return service.bulk_delete(req.ids)

