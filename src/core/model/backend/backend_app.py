from typing import List

from .background_task import BackgroundTask
from .consumer import Consumer
from .controller import Controller
from .service import Service
from core.model.backend.entity import Entity
from .value_type import StringType, NumberType, BooleanType, ValueType


class BackendApp:
    """
    Represents a backend application definition.
    """

    def __init__(self, name: str):
        self.name = name
        self._value_types = {}
        self.entities: List[Entity] = []
        self.services: List[Service] = []
        self.controllers: List[Controller] = []
        self.consumers: List[Consumer] = []
        self.bg_tasks: List[BackgroundTask] = []

        self.register_type(StringType)
        self.register_type(NumberType)
        self.register_type(BooleanType)

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def add_consumer(self, consumer: Consumer):
        self.consumers.append(consumer)

    def add_bg_task(self, task: BackgroundTask):
        self.bg_tasks.append(task)





    def has_type(self, name: str) -> bool:
        return name.lower() in self._value_types

    def get_type(self, name: str) -> ValueType:
        return self._value_types.get(name.lower())

    def register_type(self, value_type: ValueType):
        if value_type.name.lower() in self._value_types:
            raise ValueError(f"Type '{value_type.name}' is already registered.")
        self._value_types[value_type.name.lower()] = value_type

