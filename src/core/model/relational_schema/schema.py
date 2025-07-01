from typing import List

from core.model.relational_schema.table import Table


class Schema:
    """
    Represents a relational schema, which is a collection of tables.
    """

    def __init__(self, tables:List[Table]=None):
        self.tables = tables if tables is not None else []

    def add_table(self, table: Table):
        self.tables.append(table)
