from typing import Optional

class BackgroundTask:
    """
    Represents a background job.
    """
    def __init__(
        self,
        interval_seconds: int,
        handler_name: str,
        description: Optional[str] = None
    ):
        self.interval_seconds = interval_seconds
        self.handler_name = handler_name
        self.description = description
