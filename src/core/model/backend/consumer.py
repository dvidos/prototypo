from typing import Optional

class Consumer:
    """
    Represents a message consumer.
    """
    def __init__(
        self,
        queue_name: str,
        handler_name: str,
        description: Optional[str] = None
    ):
        self.queue_name = queue_name
        self.handler_name = handler_name
        self.description = description
