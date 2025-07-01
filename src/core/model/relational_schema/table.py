from typing import Optional, List

from core.model.relational_schema.column import Column
from core.model.relational_schema.foreign_key import ForeignKey
from core.model.relational_schema.index import Index


class Table:
    def __init__(
        self,
        name: str,
        primary_key: Optional[Column] = None,
        columns: List[Column] = None,
        indexes: List[Index] = None,
        foreign_keys: List[ForeignKey] = None
    ):
        self.name = name
        self.primary_key: Optional[Column] = primary_key
        self.columns: List[Column] = columns or []
        self.indexes: List[Index] = indexes or []
        self.foreign_keys: List[ForeignKey] = foreign_keys or []

    def add_column(self, column: Column):
        self.columns.append(column)

