from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.order.order import Order, OrderLine
from app.modules.order.order_service import OrderService
from app.modules.order.order_schemas import OrderCreate, OrderUpdate, OrderRead
from app.dependencies import get_db
from app.utilities.pagination import Paginator, Paginated

router = APIRouter(tags=["orders"])

@router.get("/", response_model=Paginated[OrderRead])
def list_orders(
        db: Session = Depends(get_db),
        page_num: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        sort_by: Optional[str] = Query(None),
        sort_order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
        status__ieq: Optional[str] = None,
):
    service = OrderService(db)
    [orders, pagination] = service.list_orders(
        page_num=page_num,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        status_ieq=status__ieq
    )
    return Paginated[OrderRead](pagination=pagination, results=orders)

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderRead.from_orm(order)

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = Order(
        customer_id=order_create.customer_id,
        order_lines=[OrderLine(**line.dict()) for line in order_create.order_lines],
        total=order_create.total,
        amount_paid=0
    )
    created = service.create_order(order)
    return OrderRead.from_orm(created)

@router.put("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update simple fields
    fields = order_update.dict(exclude_unset=True, exclude={"order_lines"})
    for field, value in fields.items():
        setattr(order, field, value)

    order.order_lines.clear()  # This works because of delete-orphan cascade
    for line in order_update.order_lines:
        order.order_lines.append(OrderLine(**line.dict()))

    updated = service.update_order(order)
    return OrderRead.from_orm(updated)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)) -> None:
    service = OrderService(db)
    service.delete_order(order_id)
    return

@router.post("/{order_id}/actions/confirm", response_model=OrderRead)
def confirm_order(order_id: int, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = service.confirm_order(order_id)
    return OrderRead.from_orm(order)

@router.post("/{order_id}/actions/mark_shipped", response_model=OrderRead)
def mark_order_shipped(order_id: int, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = service.mark_order_shipped(order_id)
    return OrderRead.from_orm(order)
