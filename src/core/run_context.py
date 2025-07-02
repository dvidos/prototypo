import os
from typing import Dict, List, Optional
from core.model.service_definition import ServiceDefinition
from core.model.backend.backend_app import BackendApp
from core.model.frontend.frontend_app import FrontendApp
from core.model.relational_schema.schema import Schema
from core.model.ddd.value_type import ValueType
from core.model.ddd.entity import Entity


class RunContext:
    def __init__(self, out_dir = "out"):
        self.out_dir = out_dir
        self.errors = []
        self.output = []
        self.containerized_services: Dict[ServiceDefinition] = {}
        self.containerized_volumes = []
        self.backend_app = BackendApp("backend")
        self.frontend_app = FrontendApp("frontend")
        self.db_schema = Schema()
        self.ddd_types = {}
        self.ddd_entities = []

    def error(self, message):
        self.errors.append(message)

    def print(self, message):
        self.output.append(message)

    def add_service(self, service: ServiceDefinition):
        """ Adds a service for the docker-compose file."""
        self.containerized_services[service.name] = service

    def add_volume(self, volume):
        """ Adds a volume for the docker-compose file. """
        self.containerized_volumes.append(volume)

    def write_out_file(self, out_sub_path, text):
        """Writes text to a file, splitting the path into subdir and filename."""
        subdir, filename = os.path.split(out_sub_path)
        full_dir = os.path.join(self.out_dir, subdir)
        os.makedirs(full_dir, exist_ok=True)
        full_path = os.path.join(full_dir, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(text)

    def create_out_file(self, out_sub_path):
        """Writes text to a file, splitting the path into subdir and filename."""
        subdir, filename = os.path.split(out_sub_path)
        full_dir = os.path.join(self.out_dir, subdir)
        os.makedirs(full_dir, exist_ok=True)
        full_path = os.path.join(full_dir, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            pass

    def has_type(self, name: str) -> bool:
        """ Checks if a DDD type with the given name exists. """
        return name in self.ddd_types

    def get_type(self, name: str) -> Optional[ValueType]:
        """ Returns a DDD type by name. """
        return self.ddd_types.get(name)

    def add_type(self, value_type: ValueType):
        """ Adds a DDD type to the context. """
        if value_type.name in self.ddd_types:
            self.error(f"Type '{value_type.name}' already exists.")
            return

        self.ddd_types[value_type.name] = value_type

    def has_ddd_entity(self, name: str) -> bool:
        """ Checks if a DDD entity with the given name exists. """
        return any(entity.name == name for entity in self.ddd_entities)

    def get_ddd_entity(self, name: str) -> Optional[Entity]:
        """ Returns a DDD entity by name. """
        for entity in self.ddd_entities:
            if entity.name == name:
                return entity
        return None

    def add_ddd_entity(self, entity: Entity):
        """ Adds a DDD entity to the context. """
        if self.has_ddd_entity(entity.name):
            self.error(f"Entity '{entity.name}' already exists.")
            return

        self.ddd_entities.append(entity)

