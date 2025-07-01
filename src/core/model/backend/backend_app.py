from typing import List, Optional

from .controller import Controller
from .endpoint import Endpoint
from .consumer import Consumer
from .bg_task import BackgroundTask

class BackendApp:
    """
    Represents a backend application definition.
    """

    def __init__(self, name: str):
        self.name = name
        self.controllers: List[Controller] = []
        self.consumers: List[Consumer] = []
        self.bg_tasks: List[BackgroundTask] = []

    def add_controller(self, controller: Controller):
        self.controllers.append(controller)

    def add_consumer(self, consumer: Consumer):
        self.consumers.append(consumer)

    def add_bg_task(self, task: BackgroundTask):
        self.bg_tasks.append(task)
