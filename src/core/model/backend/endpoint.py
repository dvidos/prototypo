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
        response_model: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list] = None
    ):
        self.path = path                # e.g., "/customers"
        self.method = method.upper()    # "GET", "POST"
        self.handler_name = handler_name  # function name
        self.response_model = response_model
        self.summary = summary
        self.description = description
        self.tags = tags or []
