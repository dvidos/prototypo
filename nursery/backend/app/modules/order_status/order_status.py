class OrderStatus:
    _allowed_statuses = {
        "pending": "Pending approval",
        "preparing": "Preparing for shipment",
        "shipped": "Shipped to customer",
        "delivered": "Delivered successfully"
    }

    def __init__(self, keyword: str):
        if keyword not in self._allowed_statuses:
            raise ValueError(f"Invalid order status: '{keyword}'")
        self._keyword = keyword

    @property
    def keyword(self) -> str:
        return self._keyword

    @property
    def caption(self) -> str:
        return self._allowed_statuses[self._keyword]

    def __str__(self):
        return self._keyword

    def __repr__(self):
        return f"OrderStatus({self._keyword!r})"

    def __eq__(self, other):
        return isinstance(other, OrderStatus) and self._keyword == other._keyword

    def is_final(self):
        return self._keyword == "delivered"
