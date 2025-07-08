from typing import List

from core.model.relational_schema.sql_table import SqlTable


class SqlSchema:
    """
    Represents a relational schema, which is a collection of tables.
    """

    def __init__(self, tables:List[SqlTable]=None):
        self.tables = tables if tables is not None else []

    def add_table(self, table: SqlTable):
        self.tables.append(table)
