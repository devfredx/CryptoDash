import sys
import time
import os

# --- UI IMPORTS ---
from ui.menu import Menu
from ui.menu_v2 import MenuV2
from ui.menu_map import get_guest_menu_structure

# --- REPOSITORY & AUTH IMPORTS ---
from repository.user_repository import UserRepository
from service.auth_service import AuthService

# --- SERVICE IMPORTS ---
# Legacy Services (Old Structure)
from service.market_service import MarketService
from service.wallet_service import WalletService
from service.news_service import NewsService
from service.support_service import SupportService

# New Architecture Services (Refactored)
from service.trade_service import TradeService

# --- CONTROLLER IMPORTS ---
from controllers.market_controller import MarketController
from controllers.trade_controller import TradeController


def main():
    # ---------------------------------------------------------
    # 1. INITIALIZATION
    # ---------------------------------------------------------

    # Initialize Repositories and Auth
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    # Initialize Services
    market_service = MarketService()
    wallet_service = WalletService(market_service)
    news_service = NewsService()
    support_service = SupportService()

    # Initialize New Trade Service (No arguments needed for new class)
    trade_service = TradeService()

    # Initialize Controllers
    # Market Controller needs MarketService
    market_controller = MarketController(market_service)

    # Trade Controller needs TradeService (logic) and MarketService (data)
    trade_controller = TradeController(trade_service, market_service)

    # ---------------------------------------------------------
    # 2. APPLICATION STATE
    # ---------------------------------------------------------
    current_lang = "en"
    current_session = None

    # Navigation State Management
    nav_state = {
        "mode": "dashboard",  # modes: 'dashboard', 'submenu'
        "current_key": None  # stores which submenu is active
    }

    # ---------------------------------------------------------
    # 3. MAIN LOOP
    # ---------------------------------------------------------
    while True:
        # Get dynamic menu structure based on language
        guest_mega_menu, guest_sub_menus = get_guest_menu_structure(current_lang)

        # Define UI Strings (Localization)
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

        # Determine User Label
        user_label = current_session.username if current_session else ui_guest

        # =====================================================
        # MODE: GUEST
        # =====================================================
        if current_session is None:

            # --- VIEW: DASHBOARD ---
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
                    print(f"\n   {ui_goodbye}")
                    break
                else:
                    pass  # Invalid input, loop again

            # --- VIEW: SUBMENU ---
            elif nav_state["mode"] == "submenu":
                current_key = nav_state["current_key"]

                # Fallback if key is invalid
                if current_key not in guest_sub_menus:
                    nav_state["mode"] = "dashboard"
                    continue

                menu_data = guest_sub_menus[current_key]

                # Define Breadcrumb Path
                base_path = [ui_home, menu_data["title"]]

                # Draw Submenu
                MenuV2.draw_submenu(menu_data, base_path, user_info=user_label)
                print(ui_select_sub)
                sub_choice = input(ui_input_prefix).upper().strip()

                if sub_choice in menu_data["options"]:
                    selected_option = menu_data["options"][sub_choice]
                    action = selected_option.get("action")
                    label = selected_option.get("label")

                    # -----------------------------------------
                    # ACTION ROUTER
                    # -----------------------------------------

                    # 1. Navigation Actions
                    if action and action.startswith("NAV_"):
                        nav_state["current_key"] = action.replace("NAV_", "").lower()
                        continue

                    elif action == "GO_BACK":
                        nav_state["mode"] = "dashboard"
                        nav_state["current_key"] = None

                    # 2. Language Settings
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

                    elif str(action).startswith("set_lang_"):
                        MenuV2.prepare_content_screen(base_path + ["LANGUAGE"], user_info=user_label)
                        print(f"\n 🚧 {label} coming soon!")
                        input(f"\n{ui_return_msg}")

                    # 3. Authentication Actions
                    elif action == "login":
                        t_title = "GİRİŞ" if current_lang == "tr" else "LOGIN"
                        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)
                        u_name = input("Username: ")
                        p_word = input("Password: ")
                        user = auth_service.login(u_name, p_word)
                        if user:
                            current_session = user
                            nav_state["mode"] = "dashboard"
                        else:
                            print("\n❌ Failed")
                        input(f"\n{ui_return_msg}")

                    elif action == "register":
                        t_title = "KAYIT" if current_lang == "tr" else "REGISTER"
                        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)
                        u_name = input("New Username: ")
                        p_word = input("New Password: ")
                        success, msg = auth_service.register(u_name, p_word)
                        print(f"\n📢 {msg}")
                        input(f"\n{ui_return_msg}")

                    # 4. Market Controller Actions
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

                    elif "heatmap" in str(action).lower():
                        market_controller.show_heatmap(current_lang, user_label, base_path)

                    elif "on_chain" in str(action).lower() or "onchain" in str(action).lower():
                        market_controller.show_on_chain(current_lang, user_label, base_path)

                    elif "whale" in str(action).lower():
                        market_controller.show_whale_alerts(current_lang, user_label, base_path)

                    elif "gas" in str(action).lower():
                        market_controller.show_gas_tracker(current_lang, user_label, base_path)

                    elif "calendar" in str(action).lower():
                        market_controller.view_economic_calendar(current_lang, user_label, base_path)

                    # 5. Calendar Actions (ICO & Unlocks)
                    elif action == "show_ico":
                        market_controller.show_ico_calendar(
                            current_lang,
                            user_label,
                            base_path + (["TAKVİMLER"] if current_lang == "tr" else ["CALENDARS"])
                        )

                    elif action == "show_unlocks":
                        market_controller.show_token_unlocks(
                            current_lang,
                            user_label,
                            base_path + (["TAKVİMLER"] if current_lang == "tr" else ["CALENDARS"])
                        )

                    # 6. Trade Actions (NEW: Swap)
                    elif action == "show_swap":
                        trade_controller.show_swap_tool(
                            current_lang,
                            user_label,
                            base_path + (["AL-SAT"] if current_lang == "tr" else ["TRADE"])
                        )

                    # 7. Other Services (News, FAQ)
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

                    # Default: Feature Under Construction
                    else:
                        MenuV2.prepare_content_screen(base_path + [str(label)], user_info=user_label)
                        print(f"\n[🚧] Feature '{label}' is under development")
                        input(f"\n{ui_return_msg}")

                else:
                    # Invalid submenu choice
                    pass

        # =====================================================
        # MODE: MEMBER (Simplified for Demo)
        # =====================================================
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
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   Stopped by user.")