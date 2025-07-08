from typing import Optional, Dict, List

from core.model.backend.data_model import DataModel
from core.model.backend.endpoint import Endpoint


class Action:
    def __init__(self, name: str, description: str, input_model: Optional[DataModel] = None,
                 output_model: Optional[DataModel] = None):
        self.name = name
        self.description = description
        self.input_model = input_model
        self.output_model = output_model


class Service:
    """ Represents a DDD-style Service, which is a collection of actions.
    Later we may expand into CQRS, i.e. separate handlers for commands and queries.
    """
    def __init__(
        self,
        name: Optional[str] = None,
        actions: List[Action] = None,
    ):
        self.name = name or "Service"
        self.actions = actions or []

    def add_action(self, action: Action):
        """ Adds an action to the service. """
        self.actions.append(action)