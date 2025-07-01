import os
from typing import Dict, List
from core.model.service_definition import ServiceDefinition
from core.model.backend.backend_app import BackendApp
from core.model.frontend.frontend_app import FrontendApp
from core.model.relational_schema.schema import Schema


class RunContext:
    def __init__(self, out_dir = "out"):
        self.out_dir = out_dir
        self.errors = []
        self.output = []
        self.services: Dict[ServiceDefinition] = {}
        self.volumes = []
        self.backend_app = BackendApp("backend")
        self.frontend_app = FrontendApp("frontend")
        self.db_schema = Schema()

    def error(self, message):
        self.errors.append(message)

    def print(self, message):
        self.output.append(message)

    def add_service(self, service: ServiceDefinition):
        """ Adds a service for the docker-compose file."""
        self.services[service.name] = service

    def add_volume(self, volume):
        """ Adds a volume for the docker-compose file. """
        self.volumes.append(volume)

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
