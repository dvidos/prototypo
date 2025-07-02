from enum import Enum, auto

class DataType(Enum):
    STRING = auto()
    INT = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    DATE = auto()
    TIMESTAMP = auto()
    JSON = auto()

class Column:
    def __init__(self, name: str, type: DataType, not_null=False, default=None, primary_key=False, auto_increment=False):
        self.name = name
        self.type = type
        self.not_null = not_null
        self.default = default
        self.primary_key = primary_key
        self.auto_increment = auto_increment

