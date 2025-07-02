from typing import Dict


class DataModel:
    """
    Represents a Data Model, a simple (often read-only) class
    Maybe JSON serializable, which is used to transfer data between services
    Examples are: NewCustomerRequest, CustomerResponse, etc.
    """
    def __init__(
        self,
        name: str = None,
        attributes: Dict[str, str] = None,
    ):
        self.name = name or "DataModel"
        self.attributes = attributes or {}
