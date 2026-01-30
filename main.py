from ui.menu import Menu
from ui.strings import STRINGS
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from service.market_service import MarketService
from service.wallet_service import WalletService  # <-- YENİ IMPORT


def main():
    # 1. Initialize Architecture
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)
    market_service = MarketService()

    # WalletService, fiyatları bilmek için market_service'i kullanır
    wallet_service = WalletService(market_service)  # <-- YENİ BAŞLATMA

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

            elif choice == "4":
                current_lang = "en" if current_lang == "tr" else "tr"
            elif choice == "Q":
                print(s["logout"])
                break
            else:
                Menu.show_message("Please login or register first.")
                input("\nPress Enter...")

        # --- DURUM 2: ÜYE MODU ---
        else:
            Menu.draw_member_dashboard(current_lang, current_session)
            choice = input(s["choice"]).upper()

            if choice == "1":
                all_assets = market_service.get_all_assets()
                Menu.show_market_table(all_assets)
                input("\nPress Enter to return...")

            elif choice == "2":  # <-- CUZDAN GORUNTULEME (Wallet View)
                # Cüzdan detaylarını hesapla
                summary = wallet_service.get_portfolio_summary(current_session)
                # Ekrana bas
                Menu.show_wallet_details(summary)
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