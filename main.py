# main.py

import time
# legacy imports
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

    # app state
    current_lang = "en"
    current_session = None

    # navigation state
    nav_state = {
        "mode": "dashboard",
        "current_key": None
    }

    while True:
        s = STRINGS.get(current_lang, STRINGS["en"])
        guest_mega_menu, guest_sub_menus = get_guest_menu_structure(current_lang)

        # check guest mode
        if current_session is None:

            # --- DASHBOARD VIEW ---
            if nav_state["mode"] == "dashboard":
                MenuV2.draw_mega_dashboard(guest_mega_menu)
                print(" 👉 Select (1-6) or Q:")
                choice = input("    > ").upper().strip()

                if choice in guest_mega_menu:
                    target_key = guest_mega_menu[choice]["goto"]
                    nav_state["current_key"] = target_key
                    nav_state["mode"] = "submenu"

                elif choice == "Q":
                    print("Goodbye")
                    break
                else:
                    pass

            # --- SUBMENU VIEW ---
            elif nav_state["mode"] == "submenu":
                current_key = nav_state["current_key"]

                # safety check if key exists
                if current_key not in guest_sub_menus:
                    nav_state["mode"] = "dashboard"
                    continue

                menu_data = guest_sub_menus[current_key]

                # build dynamic breadcrumb path
                base_path = ["HOME", menu_data["title"]]

                MenuV2.draw_submenu(menu_data, base_path)
                print(" 👉 Select Option:")
                sub_choice = input("    > ").upper().strip()

                if sub_choice in menu_data["options"]:
                    selected_option = menu_data["options"][sub_choice]
                    action = selected_option.get("action")
                    label = selected_option.get("label")

                    # --- ACTION HANDLERS ---

                    # 1. Navigation Logic (Deep Menus)
                    if action and action.startswith("NAV_"):
                        # switch to deeper submenu
                        # example NAV_MARKET_DATA becomes market_data
                        nav_state["current_key"] = action.replace("NAV_", "").lower()
                        # loop continues and draws new submenu
                        continue

                    # 2. Global Back Button
                    elif action == "GO_BACK":
                        # return to main dashboard
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    # 3. Language Toggle
                    elif action == "lang":
                        current_lang = "tr" if current_lang == "en" else "en"
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    # 4. Auth Actions
                    elif action == "login":
                        MenuV2.prepare_content_screen(base_path + ["LOGIN"])
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
                        MenuV2.prepare_content_screen(base_path + ["REGISTER"])
                        u_name = input("New Username: ")
                        p_word = input("New Password: ")
                        success, msg = auth_service.register(u_name, p_word)
                        print(f"\n📢 {msg}")
                        input("\nEnter to continue...")

                    # 5. Market Features
                    # mapped to new action names from menu_map
                    elif action in ["view_prices", "view_listings", "view_gainers"]:
                        MenuV2.prepare_content_screen(base_path + ["PRICES"])
                        all_assets = market_service.get_all_assets()
                        Menu.show_market_table(all_assets)
                        input("\nEnter to return...")

                    # 6. Content Features
                    elif action == "news":
                        MenuV2.prepare_content_screen(base_path + ["NEWS"])
                        news = news_service.get_latest_news(current_lang)
                        Menu.show_news(news)
                        input("\nEnter to return...")

                    elif action == "faq":
                        MenuV2.prepare_content_screen(base_path + ["FAQ"])
                        content = support_service.get_support_content(current_lang)
                        Menu.show_support_page(content)
                        input("\nEnter to return...")

                    # 7. Placeholder for Future Features
                    else:
                        MenuV2.prepare_content_screen(base_path + [label])
                        print(f"\n[🚧] Feature '{label}' is under development")
                        print("    We are working on this module")
                        input("\nEnter to continue...")

                else:
                    pass

        # member mode logic
        else:
            Menu.draw_member_dashboard(current_lang, current_session)
            choice = input("Select: ").upper()

            if choice == "O":
                current_session = None
                nav_state["mode"] = "dashboard"

            elif choice == "1":
                MenuV2.prepare_content_screen(["MEMBER", "MARKETS"])
                all_assets = market_service.get_all_assets()
                Menu.show_market_table(all_assets)
                input("\nEnter...")
            else:
                print("Option not available in demo")
                time.sleep(1)


if __name__ == "__main__":
    main()