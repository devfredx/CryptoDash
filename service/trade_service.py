from typing import Dict, Any, Optional


class TradeService:
    """
    Manages all trading operations, exchange rate calculations,
    and fee assessments for the crypto dashboard.
    """

    def __init__(self):
        # Initialize mock exchange rates (USD based)
        # In a real app, this would be fetched from an API
        self.rates: Dict[str, float] = {
            "BTC": 52000.00,
            "ETH": 3000.00,
            "BNB": 350.00,
            "SOL": 110.00,
            "AVAX": 35.50,
            "USDT": 1.00,
            "USDC": 1.00
        }

        # Define platform fee structure
        self.fee_config: Dict[str, float] = {
            "maker": 0.001,  # 0.1%
            "taker": 0.002,  # 0.2%
            "swap": 0.0015  # 0.15% fixed for swaps
        }

        print("   [SYSTEM] TradeService Initialized with mock data.")

    def _get_price(self, symbol: str) -> float:
        """
        Safely retrieve the price of an asset.
        Returns 0.0 if asset not found to prevent crashes.
        """
        return self.rates.get(symbol, 0.0)

    def validate_pair(self, source: str, target: str) -> bool:
        """
        Check if both assets exist in the system and are strictly different.
        """
        if source == target:
            return False

        if source not in self.rates or target not in self.rates:
            return False

        return True

    def get_swap_quote(self, source_sym: str, target_sym: str, amount: float) -> Dict[str, Any]:
        """
        Calculate the estimated swap output, exchange rate, and fees.

        Args:
            source_sym: Symbol of the asset being sold (e.g. 'BTC')
            target_sym: Symbol of the asset being bought (e.g. 'USDT')
            amount: Amount of source asset to swap

        Returns:
            Dictionary containing rate, fee, output amount, and fee percentage.
        """
        # Step 1: Validate input
        if not self.validate_pair(source_sym, target_sym):
            return {"error": "Invalid Pair"}

        if amount <= 0:
            return {"error": "Invalid Amount"}

        # Step 2: Get Prices
        src_price = self._get_price(source_sym)
        dst_price = self._get_price(target_sym)

        # Step 3: Calculate Exchange Rate (Source / Target)
        # Example: 1 BTC ($52000) -> ? ETH ($3000) = 17.33 ratio
        raw_rate = src_price / dst_price

        # Step 4: Calculate Output before Fees
        gross_output_amount = amount * raw_rate

        # Step 5: Calculate and Deduct Fee
        # Fee is taken from the OUTPUT asset in this model
        fee_rate = self.fee_config['swap']
        fee_amount = gross_output_amount * fee_rate

        net_output = gross_output_amount - fee_amount

        # Return structured data for the Controller
        return {
            "rate": raw_rate,
            "fee": fee_amount,
            "output": net_output,
            "fee_pct": f"{fee_rate * 100:.2f}%",
            "src_usd": src_price,
            "dst_usd": dst_price
        }