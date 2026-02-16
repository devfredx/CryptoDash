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