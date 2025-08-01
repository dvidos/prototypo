from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.order_status.order_status import OrderStatus
from app.modules.order_status.order_status_schemas import OrderStatusRead

router = APIRouter(tags=["order_statuses"])

@router.get("/", response_model=List[OrderStatusRead])
def list_statuses():
    statuses = OrderStatus.all_statuses()
    return [ OrderStatusRead(value=key, caption=statuses[key]) for key in statuses.keys() ]
