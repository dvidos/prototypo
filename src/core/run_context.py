import os
from core.model.service_definition import ServiceDefinition

class RunContext:
    def __init__(self, out_dir = "out"):
        self.out_dir = out_dir
        self.errors = []
        self.output = []
        self.services = {}
        self.volumes = []

    def error(self, message):
        self.errors.append(message)

    def print(self, message):
        self.output.append(message)

    def add_service(self, service: ServiceDefinition):
        self.services[service.name] = service

    def add_volume(self, volume):
        self.volumes.append(volume)

    def write_out_file(self, subdir, filename, text):
        full_dir = os.path.join(self.out_dir, subdir)
        os.makedirs(full_dir, exist_ok=True)  # creates dir if needed, no error if exists
        full_path = os.path.join(full_dir, filename)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(text)
