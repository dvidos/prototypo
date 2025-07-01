

class ForeignKey:
    def __init__(self, name: str, column: str, referenced_table: str, referenced_column: str):
        """
        Represents a foreign key constraint in a relational database schema.
        """
        self.name = name
        self.column = column
        self.referenced_table = referenced_table
        self.referenced_column = referenced_column

