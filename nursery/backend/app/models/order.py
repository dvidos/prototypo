from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='RESTRICT'), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False)
    status = Column(String(32), nullable=False, default="pending")  # <-- Added status field

    customer = relationship('Customer', back_populates='orders')
    order_lines = relationship('OrderLine', back_populates='order', cascade='all, delete-orphan')


class OrderLine(Base):
    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    sku = Column(String(50), nullable=False)
    description = Column(Text)
    qty = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    ext_price = Column(Numeric(12, 2), nullable=False)

    order = relationship('Order', back_populates='order_lines')
