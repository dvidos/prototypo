from typing import List, Optional


from enum import Enum, auto

class BaseType(Enum):
    TEXT = auto()
    NUMBER = auto()


class ValueType:
    """ Represents a DDD-style Value Type, a base type with restrictions.
    Such values are only compared by their value, not by identity.
    This will be used to build the types of entities and their attributes.
    """
    def __init__(self, name: str, base_type: BaseType = None):
        self.name = name
        self.base_type = base_type or BaseType.TEXT

