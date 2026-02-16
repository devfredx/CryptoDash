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

    def show_swap_tool(self, current_lang: str, user_label: str, base_path: List[str]):
        """
        Manages the multi-step swap workflow:
        Select Source -> Enter Amount -> Select Target -> Review Quote -> Confirm
        """
        ui = self._get_ui_strings(current_lang)
        MenuV2.prepare_content_screen(base_path + [ui["title"]], user_info=user_label)

        assets = self.market_service.get_all_assets()

        # --- Step 1: Select Source Asset ---
        print(f"   {C.BOLD}1. {ui['pay']}:{C.END}")
        MenuV2.draw_asset_selector(assets, current_lang)

        src_choice = input(f"\n   (0-{len(assets)}): ").strip()
        if src_choice == "0" or not src_choice.isdigit(): return
        source = assets[int(src_choice) - 1]

        # --- Step 2: Enter Amount ---
        print(f"\n   {C.BOLD}2. {ui['input_amt']} ({source['symbol']}):{C.END} ", end="")
        try:
            amt = float(input().strip())
            if amt <= 0: raise ValueError
        except ValueError:
            print(f"   {C.FAIL}{ui['invalid']}{C.END}")
            time.sleep(1)
            return

        # --- Step 3: Select Target Asset ---
        # Clear screen to keep it clean, update breadcrumb
        MenuV2.prepare_content_screen(base_path + [ui["title"], source['symbol']], user_info=user_label)
        print(f"   {C.BOLD}3. {ui['rec']}:{C.END}")
        MenuV2.draw_asset_selector(assets, current_lang)

        dst_choice = input(f"\n   (0-{len(assets)}): ").strip()
        if dst_choice == "0" or not dst_choice.isdigit(): return
        target = assets[int(dst_choice) - 1]

        # --- Step 4: Get Quote & Confirmation ---
        # Call the service we created earlier
        quote = self.trade_service.get_swap_quote(source['symbol'], target['symbol'], amt)

        # Check for service-level errors (like invalid pair)
        if "error" in quote:
            print(f"\n   {C.FAIL}ERROR: {quote['error']}{C.END}")
            time.sleep(2)
            return

        # Render Receipt
        MenuV2.prepare_content_screen(base_path + [ui["title"], "CONFIRM"], user_info=user_label)
        print(f"   {C.CYAN}{C.BOLD}{ui['receipt']}{C.END}")
        print(f"   {C.GREY}{'━' * 45}{C.END}")

        # Formatted Output
        print(f"   {ui['pay']:<15}: {C.BOLD}{amt} {source['symbol']}{C.END}")
        print(f"   {ui['rec']:<15}: {C.GREEN}{quote['output']:,.6f} {target['symbol']}{C.END}")
        print(f"   {C.GREY}{'-' * 45}{C.END}")
        print(f"   {ui['rate']:<15}: 1 {source['symbol']} ≈ {quote['rate']:,.4f} {target['symbol']}")
        print(f"   {ui['fee']:<15}: {quote['fee']:,.6f} {target['symbol']} ({quote['fee_pct']})")
        print(f"   {C.GREY}{'━' * 45}{C.END}")

        # Final Confirmation
        if input(f"\n   {ui['conf']}").lower() == 'y':
            print(f"\n   {C.GREEN}✔ {ui['succ']}{C.END}")
            time.sleep(1.5)