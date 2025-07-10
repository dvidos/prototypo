from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.base_model import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    address = Column(Text)

    orders = relationship('Order', back_populates='customer')
