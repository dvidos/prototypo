
class BuiltInType:
    STRING256 = "string256"
    INT32 = "int32"
    BIT = "bit"


class ValueType:
    """ Represents a DDD-style Value Type, a base type with restrictions.
    Such values are only compared by their value, not by identity.
    This will be used to build the types of entities and their attributes.
    """
    def __init__(self, name: str, description: str = None, base_type: str = None):
        self.name = name
        self.description = description or ""
        self.base_type = base_type or BuiltInType.STRING256


# types other value types can be based on
StringType = ValueType("String", BuiltInType.STRING256)
NumberType = ValueType("Number", BuiltInType.INT32)
BooleanType = ValueType("Boolean", BuiltInType.BIT)
