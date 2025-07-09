from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.order import Order
from app.services.order_service import OrderService
from app.schemas.order_schemas import OrderCreate, OrderUpdate, OrderRead
from app.dependencies import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    created = service.create_order(Order(**order.dict()))
    return OrderRead.from_orm(created)

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderRead.from_orm(order)

@router.put("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)) -> OrderRead:
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(order, field, value)
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
