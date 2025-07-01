from typing import List, Optional


class Component:
    """
    Represents a component in the app.
    """
    def __init__(
        self,
        component_name: str,
        component_type: str,
        description: Optional[str] = None
    ):
        self.component_name = component_name
        self.component_type = component_type
        self.description = description
        self.properties: List[str] = []  # List of properties for the component

    def add_property(self, property_name: str):
        self.properties.append(property_name)