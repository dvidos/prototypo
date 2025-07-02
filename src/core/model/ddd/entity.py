from typing import List, Optional


class Attribute:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        self.relational_schema_column = None  # This will be set later if needed
        # it could even be a list of other entities, or a N:N matrix with foreign entities.

class Entity:
    """ Represents a DDD-style Entity, which has an identifier and a collection of attributes.
    Based on this, ORMs, Controllers, HTTP/JSON DataModels, etc can be generated.
    """
    def __init__(self, name: str, id_attribute: Attribute, attributes: List[Attribute] = None):
        self.name = name
        self.id = id_attribute
        self.attributes = attributes or []
        self.relational_schema_table = None  # This will be set later if needed

    def has_attribute(self, name: str) -> bool:
        return any(attribute.name == name for attribute in self.attributes)

    def get_attribute(self, name: str) -> Optional[Attribute]:
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        return None

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)

