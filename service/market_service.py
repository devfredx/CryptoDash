from models.asset import Asset


class MarketService:
    """Manages market data and asset prices."""

    def __init__(self):
        # Initialize with dummy data for simulation
        self.assets = [
            Asset("BTC", 45000.0),
            Asset("ETH", 3200.0),
            Asset("SOL", 110.0),
            Asset("AVAX", 35.0),
            Asset("DOGE", 0.15)
        ]

    def get_all_assets(self):
        """Returns the list of all available assets."""
        return self.assets

    def get_asset_by_symbol(self, symbol):
        """Finds an asset by its symbol (e.g., BTC)."""
        for asset in self.assets:
            if asset.symbol == symbol:
                return asset
        return None