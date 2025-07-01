from typing import List
from core.model.relational_schema.column import Column


class Index:
    def __init__(self, idx_name, columns: List[Column], unique=False):
        self.idx_name = idx_name
        self.columns = columns
        self.unique = unique

