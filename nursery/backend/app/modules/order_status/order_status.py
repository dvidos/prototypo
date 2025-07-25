from typing import Dict

class OrderStatus:
    _allowed_statuses = {
        "pending": "Pending approval",
        "preparing": "Preparing for shipment",
        "shipped": "Shipped to customer",
        "delivered": "Delivered successfully"
    }

    def __init__(self, value: str):
        if value not in self._allowed_statuses:
            raise ValueError(f"Invalid order status: '{value}'")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def caption(self) -> str:
        return self._allowed_statuses[self._value]

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"OrderStatus({self._value!r})"

    def __eq__(self, other):
        return isinstance(other, OrderStatus) and self._value == other._value

    def is_final(self):
        return self._value == "delivered"

    @classmethod
    def all_statuses(cls) -> Dict[str, str]:
        return OrderStatus._allowed_statuses

