from typing import List, Optional

from core.model.backend.value_type import ValueType
from core.model.relational_schema.sql_table import SqlTable


class Attribute:
    def __init__(self, name: str, type: ValueType):
        self.name = name
        self.type: ValueType = type
        # it could even be a list of other entities, or a N:N matrix with foreign entities.
        self.related_sql_column = None  # This will be set later if needed



class Entity:
    """ Represents a DDD-style Entity, which has an identifier and a collection of attributes.
    Based on this, ORMs, Controllers, HTTP/JSON DataModels, etc can be generated.
    """
    def __init__(self, name: str, id_attribute: Attribute, attributes: List[Attribute] = None):
        self.name = name
        self.id = id_attribute
        self.attributes = attributes or []
        self.related_sql_table: SqlTable = None  # This will be set later if needed
        self.related_controller = None  # This will be set later if needed
        self.related_service = None  # This will be set later if needed


    def has_attribute(self, name: str) -> bool:
        return any(attribute.name == name for attribute in self.attributes)

    def get_attribute(self, name: str) -> Optional[Attribute]:
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        return None

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)


