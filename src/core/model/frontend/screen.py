from typing import Optional

class Screen:
    """
    Represents a screen in the app.
    """
    def __init__(
        self,
        screen_name: str
    ):
        self.screen_name = screen_name
        self.description: Optional[str] = None
        self.components: list = []
