from datetime import datetime  # <-- YENİ EKLENDİ (Tarih için gerekli)


class TradeService:
    """Handles buying and selling of crypto assets."""

    def __init__(self, market_service, user_repository):
        self.market_service = market_service
        self.user_repository = user_repository

    def _add_to_history(self, user, type, symbol, amount, price, total):
        """Helper method to record transaction (YENİ METOD)."""
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": type,
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "total": total
        }
        # Kullanıcının history listesine ekle
        user.history.append(record)

    def buy_asset(self, user, symbol, amount_usdt):
        """
        Buys a crypto asset using USDT balance.
        """
        # 1. Validate Asset
        asset = self.market_service.get_asset_by_symbol(symbol)
        if not asset:
            return False, "Invalid asset symbol!"

        # 2. Validate Balance
        if user.balance < amount_usdt:
            return False, f"Insufficient balance! You have {user.balance} USDT."

        # 3. Calculate Coin Amount
        coin_amount = amount_usdt / asset.current_price

        # 4. Execute Trade
        user.balance -= amount_usdt  # Decrease Money

        # Add Coin to Wallet (Initialize if not exists)
        if symbol not in user.assets:
            user.assets[symbol] = 0.0
        user.assets[symbol] += coin_amount

        # 5. RECORD HISTORY (GEÇMİŞE KAYDET)
        self._add_to_history(user, "BUY", symbol, coin_amount, asset.current_price, amount_usdt)

        return True, f"Bought {coin_amount:.4f} {symbol} for {amount_usdt} USDT."

    def sell_asset(self, user, symbol, amount_coin):
        """
        Sells a crypto asset for USDT.
        """
        # 1. Validate Asset
        asset = self.market_service.get_asset_by_symbol(symbol)
        if not asset:
            return False, "Invalid asset symbol!"

        # 2. Validate Portfolio
        current_coin_balance = user.assets.get(symbol, 0.0)
        if current_coin_balance < amount_coin:
            return False, f"Insufficient {symbol}! You have {current_coin_balance}."

        # 3. Calculate USDT Value
        usdt_value = amount_coin * asset.current_price

        # 4. Execute Trade
        user.assets[symbol] -= amount_coin  # Decrease Coin
        user.balance += usdt_value  # Increase Money

        # Remove key if balance is zero (clean up)
        if user.assets[symbol] <= 0:
            del user.assets[symbol]

        # 5. RECORD HISTORY (GEÇMİŞE KAYDET)
        self._add_to_history(user, "SELL", symbol, amount_coin, asset.current_price, usdt_value)

        return True, f"Sold {amount_coin:.4f} {symbol} for {usdt_value:.2f} USDT."