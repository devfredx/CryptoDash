import time
from typing import List, Dict, Any
from ui.menu_v2 import MenuV2, C


class TradeController:
    """
    Handles user interactions for trading features (Swap, Spot, etc.).
    Bridges the UI (MenuV2) with the Logic (TradeService).
    """

    def __init__(self, trade_service: Any, market_service: Any):
        # Inject services to access logic and data
        self.trade_service = trade_service
        self.market_service = market_service

    def _get_ui_strings(self, lang: str) -> Dict[str, str]:
        """
        Returns localized UI labels for the trade module.
        """
        if lang == "tr":
            return {
                "title": "KOLAY AL/SAT (SWAP)",
                "pay": "ÖDENEN",
                "rec": "ALINAN",
                "rate": "KUR",
                "fee": "KOMİSYON",
                "conf": "İşlemi Onayla? (y/n): ",
                "succ": "Takas Başarılı!",
                "input_amt": "Miktar Girin",
                "receipt": "İŞLEM MAKBUZU",
                "invalid": "Geçersiz Giriş!"
            }
        return {
            "title": "EASY SWAP",
            "pay": "PAY",
            "rec": "RECEIVE",
            "rate": "RATE",
            "fee": "FEE",
            "conf": "Confirm Swap? (y/n): ",
            "succ": "Swap Successful!",
            "input_amt": "Enter Amount",
            "receipt": "SWAP RECEIPT",
            "invalid": "Invalid Input!"
        }