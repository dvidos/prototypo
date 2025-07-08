from typing import List, Optional
from sqlalchemy.orm import Session
from .entity import {{entity.name}}

class {{ entity.name }}Repository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: {{entity.name}}):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get(self, item_id: int) -> Optional[{{entity.name}}]:
        return self.db.query({{entity.name}}).filter({{entity.name}}.id == item_id).first()

    def update(self, item: {{entity.name}}):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int):
        item = self.get(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    def list(self, skip: int = 0, limit: int = 100) -> List[{{entity.name}}]:
        return self.db.query({{entity.name}}).offset(skip).limit(limit).all()

    def filter(self, **kwargs) -> List[{{entity.name}}]:
        query = self.db.query({{entity.name}})
        for key, value in kwargs.items():
            if hasattr({{entity.name}}, key):
                query = query.filter(getattr({{entity.name}}, key) == value)
        return query.all()

