from typing import Optional, Dict

from core.model.backend.endpoint import Endpoint


class DataModel:
    """
    Represents a Data Model, a simple (often read-only) class
    Examples are: NewCustomerRequest, CustomerResponse, etc.
    """
    def __init__(
        self,
        name: str = None,
        attributes: Dict[str, str] = None,
    ):
        self.name = name or "DataModel"
        self.attributes = attributes or {}
