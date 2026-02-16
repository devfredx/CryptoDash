from typing import Dict, Any, Optional

class TradeService:
    """
    Manages all trading operations, exchange rate calculations,
    and fee assessments for the crypto dashboard.
    """

    def __init__(self):
        # Initialize mock exchange rates (USD based)
        # Comprehensive list of major assets to prevent missing price errors
        self.rates: Dict[str, float] = {
            "BTC": 64500.00,
            "ETH": 3450.00,
            "BNB": 590.00,
            "SOL": 145.00,
            "XRP": 0.62,
            "ADA": 0.45,
            "AVAX": 48.20,
            "DOGE": 0.16,
            "DOT": 8.50,
            "TRX": 0.12,
            "LINK": 18.40,
            "MATIC": 0.95,
            "SHIB": 0.000025,
            "LTC": 85.00,
            "UNI": 12.00,
            "ARB": 1.12,
            "OP": 2.50,
            "SUI": 1.65,
            "APT": 14.20,
            "FIL": 8.50,
            "NEAR": 6.20,
            "STX": 2.80,
            "IMX": 2.10,
            "KAS": 0.13,
            "USDT": 1.00,
            "USDC": 1.00,
            "DAI": 1.00,
            "FDUSD": 1.00
        }

        # Define platform fee structure
        self.fee_config: Dict[str, float] = {
            "maker": 0.001,  # 0.1%
            "taker": 0.002,  # 0.2%
            "swap": 0.0015   # 0.15% fixed for swaps
        }

        print("   [SYSTEM] TradeService Initialized.")

    def _get_price(self, symbol: str) -> float:
        """
        Safely retrieve the price of an asset.
        Returns 0.0 if asset not found.
        """
        # Normalize symbol: strip whitespace and convert to uppercase
        # This ensures "btc ", "BTC ", and "btc" are all treated as "BTC"
        clean_symbol = str(symbol).strip().upper()

        return self.rates.get(clean_symbol, 0.0)

    def validate_pair(self, source: str, target: str) -> bool:
        """
        Check if pair is valid (different assets).
        """
        # Normalize symbols before comparison
        s = str(source).strip().upper()
        t = str(target).strip().upper()

        if s == t:
            return False
        return True

    def get_swap_quote(self, source_sym: str, target_sym: str, amount: float) -> Dict[str, Any]:
        """
        Calculate the estimated swap output, exchange rate, and fees.
        """
        # Step 1: Validate input basics
        if not self.validate_pair(source_sym, target_sym):
            return {"error": "Same Asset"}

        if amount <= 0:
            return {"error": "Invalid Amount"}

        # Step 2: Get Prices
        src_price = self._get_price(source_sym)
        dst_price = self._get_price(target_sym)

        # Check for missing prices (0.0 indicates asset not found in rate map)
        if src_price == 0.0:
            return {"error": f"Price not found: '{source_sym}'"}

        if dst_price == 0.0:
            return {"error": f"Price not found: '{target_sym}'"}

        # Step 3: Calculate Exchange Rate (Source / Target)
        try:
            raw_rate = src_price / dst_price
        except ZeroDivisionError:
            return {"error": "Market Error (Zero Price)"}

        # Step 4: Calculate Output before Fees
        gross_output_amount = amount * raw_rate

        # Step 5: Calculate and Deduct Fee
        fee_rate = self.fee_config['swap']
        fee_amount = gross_output_amount * fee_rate

        net_output = gross_output_amount - fee_amount

        # Return structured data
        return {
            "rate": raw_rate,
            "fee": fee_amount,
            "output": net_output,
            "fee_pct": f"{fee_rate * 100:.2f}%",
            "src_usd": src_price,
            "dst_usd": dst_price
        }