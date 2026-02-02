# main.py

import time
# legacy imports for services
from ui.menu import Menu
from ui.strings import STRINGS
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from service.market_service import MarketService
from service.wallet_service import WalletService
from service.trade_service import TradeService
from service.news_service import NewsService
from service.support_service import SupportService

# v2 imports
from ui.menu_map import get_guest_menu_structure
from ui.menu_v2 import MenuV2


def main():
    # initialize services
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)
    market_service = MarketService()
    wallet_service = WalletService(market_service)
    trade_service = TradeService(market_service, user_repo)
    news_service = NewsService()
    support_service = SupportService()

    # application state
    # default language is english
    current_lang = "en"
    current_session = None

    # navigation state
    nav_state = {
        "mode": "dashboard",
        "current_key": None
    }

    while True:
        # load strings for legacy support
        s = STRINGS.get(current_lang, STRINGS["en"])

        # load v2 menu structure based on current language
        guest_mega_menu, guest_sub_menus = get_guest_menu_structure(current_lang)

        # check guest mode
        if current_session is None:

            # dashboard view
            if nav_state["mode"] == "dashboard":
                MenuV2.draw_mega_dashboard(guest_mega_menu)
                choice = input(" 👉 Select (1-6) or Q: ").upper().strip()

                if choice in guest_mega_menu:
                    target_key = guest_mega_menu[choice]["goto"]
                    nav_state["current_key"] = target_key
                    nav_state["mode"] = "submenu"

                elif choice == "Q":
                    print("Goodbye")
                    break
                else:
                    # invalid input refresh
                    pass

            # submenu view
            elif nav_state["mode"] == "submenu":
                current_key = nav_state["current_key"]
                menu_data = guest_sub_menus[current_key]

                # build breadcrumb path
                path = ["HOME", menu_data["title"]]

                MenuV2.draw_submenu(menu_data, path)
                sub_choice = input(" 👉 Select: ").upper().strip()

                if sub_choice in menu_data["options"]:
                    selected_option = menu_data["options"][sub_choice]
                    action = selected_option.get("action")

                    # handle actions

                    if action == "GO_BACK":
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    elif action == "lang":
                        # toggle language en to tr or tr to en
                        current_lang = "tr" if current_lang == "en" else "en"
                        print(f"Language changed to {current_lang.upper()}")
                        time.sleep(0.5)
                        # return to dashboard to see changes
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    elif action == "login":
                        MenuV2.clear_screen()
                        print(f"--- LOGIN ---")
                        u_name = input("Username: ")
                        p_word = input("Password: ")
                        user = auth_service.login(u_name, p_word)
                        if user:
                            current_session = user
                            print(f"\n✅ Success")
                            nav_state["mode"] = "dashboard"
                        else:
                            print(f"\n❌ Failed")
                        input("\nEnter to continue...")

                    elif action == "register":
                        MenuV2.clear_screen()
                        print(f"--- REGISTER ---")
                        u_name = input("New Username: ")
                        p_word = input("New Password: ")
                        success, msg = auth_service.register(u_name, p_word)
                        print(f"\n📢 {msg}")
                        input("\nEnter to continue...")

                    elif action == "market_data":
                        all_assets = market_service.get_all_assets()
                        # using legacy table drawer
                        Menu.show_market_table(all_assets)
                        input("\nEnter to return...")

                    elif action == "news":
                        news = news_service.get_latest_news(current_lang)
                        Menu.show_news(news)
                        input("\nEnter to return...")

                    elif action == "faq":
                        content = support_service.get_support_content(current_lang)
                        Menu.show_support_page(content)
                        input("\nEnter to return...")

                    else:
                        print(f"\n[🚧] Feature under development")
                        input("Enter to continue...")

                else:
                    pass

        # member mode logic
        else:
            # legacy member dashboard
            # will be updated to v2 later
            Menu.draw_member_dashboard(current_lang, current_session)
            choice = input("Select: ").upper()

            if choice == "O":
                current_session = None
                nav_state["mode"] = "dashboard"
                print("\n👋 Logout")
                time.sleep(1)

            # basic logout handling for now
            # other member features remain same as legacy code
            elif choice == "1":
                all_assets = market_service.get_all_assets()
                Menu.show_market_table(all_assets)
                input("\nEnter...")
            else:
                print("Option not available in demo")
                time.sleep(1)


if __name__ == "__main__":
    main()