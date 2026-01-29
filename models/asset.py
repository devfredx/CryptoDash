class Asset:
    """Represents a crypto asset with symbol and price."""

    def __init__(self, symbol, current_price):
        self.symbol = symbol
        self.current_price = current_price

    def __str__(self):
        return f"{self.symbol}: ${self.current_price}"