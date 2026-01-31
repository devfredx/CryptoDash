from ui.menu import Menu
from ui.strings import STRINGS
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from service.market_service import MarketService
from service.wallet_service import WalletService
from service.trade_service import TradeService
from service.news_service import NewsService


def main():
    # 1. Initialize Architecture
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)
    market_service = MarketService()
    wallet_service = WalletService(market_service)
    trade_service = TradeService(market_service, user_repo)
    news_service = NewsService()

    # 2. Application State
    current_lang = "tr"
    current_session = None

    while True:
        s = STRINGS[current_lang]

        # --- DURUM 1: MİSAFİR MODU ---
        if current_session is None:
            Menu.draw_guest_dashboard(current_lang)
            choice = input(s["choice"]).upper()

            if choice == "1":
                all_assets = market_service.get_all_assets()
                Menu.show_market_table(all_assets)
                input("\nPress Enter to return...")

            elif choice == "4":  # <-- HABERLER (DİL DESTEKLİ)
                # Buraya current_lang parametresini ekledik
                news = news_service.get_latest_news(current_lang)
                Menu.show_news(news)
                input("\nPress Enter to return...")

            elif choice == "R":
                Menu.clear_screen()
                print(f"--- {s['m_register'].upper()} ---")
                u_name = input(f"{s['choice']} (Username): ")
                p_word = input(f"{s['choice']} (Password): ")
                success, msg = auth_service.register(u_name, p_word)
                Menu.show_message(msg)
                input("\nPress Enter...")

            elif choice == "L":
                Menu.clear_screen()
                print(f"--- {s['m_login'].upper()} ---")
                u_name = input(f"{s['choice']} (Username): ")
                p_word = input(f"{s['choice']} (Password): ")
                user = auth_service.login(u_name, p_word)
                if user:
                    current_session = user
                    Menu.show_message(s["login_success"])
                else:
                    Menu.show_message(s["login_fail"])
                input("\nPress Enter...")

            elif choice == "9":  # <-- DİL DEĞİŞTİRME
                current_lang = "en" if current_lang == "tr" else "tr"

            elif choice == "Q":
                print(s["logout"])
                break
            else:
                Menu.show_message(s["invalid"])

        # --- DURUM 2: ÜYE MODU ---
        else:
            Menu.draw_member_dashboard(current_lang, current_session)
            choice = input(s["choice"]).upper()

            if choice == "1":
                all_assets = market_service.get_all_assets()
                Menu.show_market_table(all_assets)
                input("\nPress Enter to return...")

            elif choice == "2":
                summary = wallet_service.get_portfolio_summary(current_session)
                Menu.show_wallet_details(summary)
                input("\nPress Enter to return...")

            elif choice == "3":
                Menu.draw_trade_menu()
                sub_choice = input(s["choice"]).upper()

                if sub_choice == "B":  # BUY
                    symbol = input("Coin Symbol (e.g. BTC): ").upper()
                    try:
                        amount = float(input("Amount in USDT: "))
                        success, msg = trade_service.buy_asset(current_session, symbol, amount)
                        Menu.show_message(msg)
                    except ValueError:
                        Menu.show_message("Invalid number format!")

                elif sub_choice == "S":  # SELL
                    symbol = input("Coin Symbol (e.g. BTC): ").upper()
                    try:
                        amount = float(input("Amount to Sell: "))
                        success, msg = trade_service.sell_asset(current_session, symbol, amount)
                        Menu.show_message(msg)
                    except ValueError:
                        Menu.show_message("Invalid number format!")

                input("\nPress Enter to return...")

            elif choice == "4":  # <-- HABERLER (DİL DESTEKLİ)
                # Buraya da current_lang parametresini ekledik
                news = news_service.get_latest_news(current_lang)
                Menu.show_news(news)
                input("\nPress Enter to return...")

            elif choice == "5":
                Menu.show_history(current_session.history)
                input("\nPress Enter to return...")

            elif choice == "O":
                current_session = None
                Menu.show_message(s["logout"])
                input("\nPress Enter...")

            else:
                Menu.show_message("Feature coming soon...")
                input("\nPress Enter...")


if __name__ == "__main__":
    main()