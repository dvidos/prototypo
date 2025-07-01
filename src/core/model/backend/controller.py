from typing import Optional, Dict, List

from core.model.backend.data_model import DataModel
from core.model.backend.endpoint import Endpoint


class Controller:
    """
    Represents a collection of HTTP endpoints for a specific resource.
    """
    def __init__(
        self,
        name: Optional[str] = None,
        models: List[DataModel] = None,
        endpoints: List[Endpoint] = None
    ):
        self.name = name or "Controller"
        self.models = models or []
        self.endpoints = endpoints or []

