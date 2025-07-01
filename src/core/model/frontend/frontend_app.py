from typing import List, Optional
from .screen import Screen
from .component import Component

class FrontendApp:
    """
    Represents a front end application definition.
    """

    def __init__(self, name: str):
        self.name = name
        self.components: List[Component] = []
        self.screens: List[Screen] = []

    def add_component(self, component: Component):
        self.components.append(component)

    def add_screen(self, screen: Screen):
        self.screens.append(screen)
