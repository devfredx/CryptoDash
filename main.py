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
from ui.menu_v2 import MenuV2, C


# helper function for formatting numbers
def format_large_number(num):
    # formats 1,000,000 to 1.0M, 1,000,000,000 to 1.0B
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    return str(num)


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

            # dashboard view
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

            # submenu view
            elif nav_state["mode"] == "submenu":
                current_key = nav_state["current_key"]

                if current_key not in guest_sub_menus:
                    nav_state["mode"] = "dashboard"
                    continue

                menu_data = guest_sub_menus[current_key]
                base_path = ["HOME", menu_data["title"]]

                MenuV2.draw_submenu(menu_data, base_path)
                print(" 👉 Select Option:")
                sub_choice = input("    > ").upper().strip()

                if sub_choice in menu_data["options"]:
                    selected_option = menu_data["options"][sub_choice]
                    action = selected_option.get("action")
                    label = selected_option.get("label")

                    # action handlers

                    # navigation logic
                    if action and action.startswith("NAV_"):
                        nav_state["current_key"] = action.replace("NAV_", "").lower()
                        continue

                    # back logic
                    elif action == "GO_BACK":
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    # language settings
                    elif action == "set_lang_en":
                        current_lang = "en"
                        print("\n✅ Language set to English")
                        time.sleep(0.5)
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    elif action == "set_lang_tr":
                        current_lang = "tr"
                        print("\n✅ Dil Türkçe olarak ayarlandı")
                        time.sleep(0.5)
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    elif action in ["set_lang_de", "set_lang_es", "set_lang_ru", "set_lang_zh"]:
                        MenuV2.prepare_content_screen(base_path + ["LANGUAGE"])
                        print(f"\n 🚧 {label} coming soon!")
                        input("\nEnter to continue...")

                    # auth logic
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

                    # --- MARKET DATA FEATURES (UPDATED) ---
                    elif action == "view_prices":
                        MenuV2.prepare_content_screen(base_path + ["CRYPTO PRICES"])

                        # fetch rich data
                        data = market_service.get_top_coins()

                        # modern table headers
                        headers = ["#", "ASSET", "PRICE", "24H %", "M. CAP", "VOL (24H)"]
                        # adjust widths for better spacing
                        widths = [4, 16, 14, 12, 12, 12]

                        table_rows = []

                        for coin in data:
                            # format change with arrow
                            change_val = coin['change']
                            arrow = "▲" if change_val >= 0 else "▼"
                            change_str = f"{arrow} {change_val}%"

                            # format asset name like "BTC • Bitcoin"
                            asset_str = f"{coin['symbol']} • {coin['name']}"

                            row = [
                                str(coin["rank"]),  # #
                                asset_str,  # ASSET
                                f"${coin['price']:,.2f}",  # PRICE
                                change_str,  # 24H %
                                format_large_number(coin["mcap"]),  # M. CAP
                                format_large_number(coin["vol"])  # VOL
                            ]
                            table_rows.append(row)

                        MenuV2.draw_table(headers, table_rows, widths)
                        input("\nEnter to return...")

                    elif action == "view_listings":
                        MenuV2.prepare_content_screen(base_path + ["NEW LISTINGS"])

                        data = market_service.get_new_listings()
                        headers = ["Symbol", "Name", "List Price", "Performance", "Listed"]
                        widths = [10, 15, 15, 15, 15]
                        table_rows = []

                        for coin in data:
                            row = [coin["symbol"], coin["name"], f"${coin['price']}", f"{coin['change']}%",
                                   coin["date"]]
                            table_rows.append(row)

                        MenuV2.draw_table(headers, table_rows, widths)
                        input("\nEnter to return...")

                    elif action == "view_gainers":
                        MenuV2.prepare_content_screen(base_path + ["GAINERS & LOSERS"])
                        gainers, losers = market_service.get_gainers_losers()

                        print(f"   {C.GREEN}🚀 TOP GAINERS{C.END}")
                        for g in gainers:
                            print(f"   • {g['symbol']:<10} {C.GREEN}+{g['change']}%{C.END} (${g['price']})")

                        print(f"\n   {C.FAIL}📉 TOP LOSERS{C.END}")
                        for l in losers:
                            print(f"   • {l['symbol']:<10} {C.FAIL}{l['change']}%{C.END} (${l['price']})")

                        input("\n\nEnter to return...")

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

                    else:
                        MenuV2.prepare_content_screen(base_path + [label])
                        print(f"\n[🚧] Feature '{label}' is under development")
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