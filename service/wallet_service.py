class WalletService:
    """Handles calculation of user assets and total wealth."""

    def __init__(self, market_service):
        # Fiyatları bilmek için MarketService'e ihtiyacımız var
        self.market_service = market_service

    def get_portfolio_summary(self, user):
        """Calculates value of all crypto assets owned by user."""
        asset_details = []
        total_crypto_value = 0.0

        # Kullanıcının varlıklarını dön (Örn: {'BTC': 0.5})
        for symbol, amount in user.assets.items():
            # Güncel fiyatı al
            asset = self.market_service.get_asset_by_symbol(symbol)
            if asset:
                current_value = amount * asset.current_price
                total_crypto_value += current_value

                asset_details.append({
                    "symbol": symbol,
                    "amount": amount,
                    "price": asset.current_price,
                    "total_value": current_value
                })

        total_wealth = user.balance + total_crypto_value

        return {
            "balance_usdt": user.balance,
            "crypto_total": total_crypto_value,
            "total_wealth": total_wealth,
            "assets": asset_details
        }