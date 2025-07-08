from typing import Optional, Dict

from core.model.backend.data_model import DataModel


class MessageQueue:
    """
    Represents a message queue
    """
    def __init__(
        self,
        name: str,
        message_model: Optional[DataModel] = None,
    ):
        self.name = name                # e.g., "customer_created"
        self.message_model = message_model    # "GET", "POST"
