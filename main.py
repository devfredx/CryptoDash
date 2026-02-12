# main.py

import time

# Legacy imports
from ui.menu import Menu
from ui.strings import STRINGS
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from service.market_service import MarketService
from service.wallet_service import WalletService
from service.trade_service import TradeService
from service.news_service import NewsService
from service.support_service import SupportService

# V2 imports
from ui.menu_map import get_guest_menu_structure
from ui.menu_v2 import MenuV2

# Controllers
from controllers.market_controller import MarketController


def main():
    # Initialize services
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)
    market_service = MarketService()
    wallet_service = WalletService(market_service)
    trade_service = TradeService(market_service, user_repo)
    news_service = NewsService()
    support_service = SupportService()

    # Initialize Controllers
    market_controller = MarketController(market_service)

    # App state
    current_lang = "en"
    current_session = None

    # Navigation state
    nav_state = {
        "mode": "dashboard",
        "current_key": None
    }

    while True:
        s = STRINGS.get(current_lang, STRINGS["en"])
        guest_mega_menu, guest_sub_menus = get_guest_menu_structure(current_lang)

        # UI translation logic
        if current_lang == "tr":
            ui_home = "ANASAYFA"
            ui_guest = "Misafir"
            ui_select_main = " 👉 Seçim (1-6) veya Q:"
            ui_select_sub = " 👉 Seçim Yapınız:"
            ui_input_prefix = "    > "
            ui_return_msg = "Geri dönmek için Enter..."
            ui_goodbye = "Güle güle..."
            ui_footer = "[Sütun Seçimi: 1-6]"
        else:
            ui_home = "HOME"
            ui_guest = "Guest"
            ui_select_main = " 👉 Select (1-6) or Q:"
            ui_select_sub = " 👉 Select Option:"
            ui_input_prefix = "    > "
            ui_return_msg = "Enter to return..."
            ui_goodbye = "Goodbye"
            ui_footer = "[Select Column: 1-6]"

        # Determine user label
        user_label = current_session.username if current_session else ui_guest

        # Check guest mode
        if current_session is None:

            # Dashboard view
            if nav_state["mode"] == "dashboard":
                MenuV2.draw_mega_dashboard(
                    guest_mega_menu,
                    page_title=ui_home,
                    user_info=user_label,
                    footer_text=ui_footer
                )

                print(ui_select_main)
                choice = input(ui_input_prefix).upper().strip()

                if choice in guest_mega_menu:
                    target_key = guest_mega_menu[choice]["goto"]
                    nav_state["current_key"] = target_key
                    nav_state["mode"] = "submenu"

                elif choice == "Q":
                    print(ui_goodbye)
                    break
                else:
                    pass

            # Submenu view
            elif nav_state["mode"] == "submenu":
                current_key = nav_state["current_key"]

                if current_key not in guest_sub_menus:
                    nav_state["mode"] = "dashboard"
                    continue

                menu_data = guest_sub_menus[current_key]
                base_path = [ui_home, menu_data["title"]]

                MenuV2.draw_submenu(menu_data, base_path, user_info=user_label)
                print(ui_select_sub)
                sub_choice = input(ui_input_prefix).upper().strip()

                if sub_choice in menu_data["options"]:
                    selected_option = menu_data["options"][sub_choice]
                    action = selected_option.get("action")
                    label = selected_option.get("label")

                    # --- CONTROLLER ROUTING LOGIC ---

                    # Navigation logic
                    if action and action.startswith("NAV_"):
                        nav_state["current_key"] = action.replace("NAV_", "").lower()
                        continue

                    # Back logic
                    elif action == "GO_BACK":
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    # Language settings
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
                        MenuV2.prepare_content_screen(base_path + ["LANGUAGE"], user_info=user_label)
                        print(f"\n 🚧 {label} coming soon!")
                        input(f"\n{ui_return_msg}")

                    # Auth logic
                    elif action == "login":
                        t_title = "GİRİŞ" if current_lang == "tr" else "LOGIN"
                        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)
                        prompt_u = "Kullanıcı Adı: " if current_lang == "tr" else "Username: "
                        prompt_p = "Şifre: " if current_lang == "tr" else "Password: "
                        u_name = input(prompt_u)
                        p_word = input(prompt_p)
                        user = auth_service.login(u_name, p_word)
                        if user:
                            current_session = user
                            print(f"\n✅ Success")
                            nav_state["mode"] = "dashboard"
                        else:
                            print(f"\n❌ Failed")
                        input(f"\n{ui_return_msg}")

                    elif action == "register":
                        t_title = "KAYIT" if current_lang == "tr" else "REGISTER"
                        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)
                        prompt_u = "Yeni Kullanıcı Adı: " if current_lang == "tr" else "New Username: "
                        prompt_p = "Yeni Şifre: " if current_lang == "tr" else "New Password: "
                        u_name = input(prompt_u)
                        p_word = input(prompt_p)
                        success, msg = auth_service.register(u_name, p_word)
                        print(f"\n📢 {msg}")
                        input(f"\n{ui_return_msg}")

                    # --- MARKET CONTROLLER DELEGATION ---
                    elif action == "view_prices":
                        market_controller.view_prices(current_lang, user_label, base_path)

                    elif action == "view_listings":
                        market_controller.view_listings(current_lang, user_label, base_path)

                    elif action == "view_gainers":
                        market_controller.view_gainers(current_lang, user_label, base_path)

                    elif action == "view_sectors":
                        market_controller.view_sectors(current_lang, user_label, base_path)

                    elif action == "view_fear_greed":
                        market_controller.view_fear_greed(current_lang, user_label, base_path)

                    elif action == "show_chart":
                        market_controller.show_chart(current_lang, user_label, base_path)

                    elif "heatmap" in action.lower():
                        market_controller.show_heatmap(current_lang, user_label, base_path)

                    elif "on_chain" in action.lower() or "onchain" in action.lower():
                        market_controller.show_on_chain(current_lang, user_label, base_path)

                    # --- OTHER SERVICES ---
                    elif action == "news":
                        MenuV2.prepare_content_screen(base_path + ["NEWS"], user_info=user_label)
                        news = news_service.get_latest_news(current_lang)
                        Menu.show_news(news)
                        input(f"\n{ui_return_msg}")

                    elif action == "faq":
                        MenuV2.prepare_content_screen(base_path + ["FAQ"], user_info=user_label)
                        content = support_service.get_support_content(current_lang)
                        Menu.show_support_page(content)
                        input(f"\n{ui_return_msg}")

                    else:
                        MenuV2.prepare_content_screen(base_path + [label], user_info=user_label)
                        print(f"\n[🚧] Feature '{label}' is under development")
                        input(f"\n{ui_return_msg}")

                else:
                    pass

        # Member mode logic
        else:
            Menu.draw_member_dashboard(current_lang, current_session)
            choice = input("Select: ").upper()
            if choice == "O":
                current_session = None
                nav_state["mode"] = "dashboard"
            elif choice == "1":
                MenuV2.prepare_content_screen(["MEMBER", "MARKETS"], user_info=user_label)
                all_assets = market_service.get_all_assets()
                Menu.show_market_table(all_assets)
                input("\nEnter...")
            else:
                print("Option not available in demo")
                time.sleep(1)

if __name__ == "__main__":
    main()