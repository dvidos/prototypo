from typing import Optional, Dict

class Endpoint:
    """
    Represents an HTTP endpoint.
    """
    def __init__(
        self,
        path: str,
        method: str,
        handler_name: str,
        identifier_name: Optional[str] = None,
        request_model: Optional[str] = None,
        response_model: Optional[str] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        tags: Optional[list] = None
    ):
        self.path = path                # e.g., "/customers"
        self.method = method.upper()    # "GET", "POST"
        self.handler_name = handler_name  # function name
        self.identifier_name = identifier_name  # e.g., "id" for "/customers/{id}"
        self.request_model = request_model  # e.g., "CustomerCreateRequest"
        self.response_model = response_model  # e.g., "CustomerResponse"
        self.name = name               # e.g., "Create Customer"
        self.summary = summary         # e.g., "Create a new Customer"
        self.tags = tags or []
