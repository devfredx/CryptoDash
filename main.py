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
from ui.menu_v2 import MenuV2, C


# Helper function for number formatting
def format_large_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    return str(num)


def main():
    # Initialize services
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)
    market_service = MarketService()
    wallet_service = WalletService(market_service)
    trade_service = TradeService(market_service, user_repo)
    news_service = NewsService()
    support_service = SupportService()

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

                    # Action handlers

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

                    # Market data features
                    elif action == "view_prices":
                        title = "KRİPTO FİYATLARI" if current_lang == "tr" else "CRYPTO PRICES"
                        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

                        data = market_service.get_top_coins()

                        if current_lang == "tr":
                            headers = ["#", "VARLIK", "FİYAT", "24S %", "P. DEĞERİ", "HACİM (24S)"]
                        else:
                            headers = ["#", "ASSET", "PRICE", "24H %", "M. CAP", "VOL (24H)"]

                        widths = [4, 16, 14, 12, 12, 12]
                        table_rows = []

                        for coin in data:
                            change_val = coin['change']
                            arrow = "▲" if change_val >= 0 else "▼"
                            change_str = f"{arrow} {change_val}%"
                            asset_str = f"{coin['symbol']} • {coin['name']}"

                            row = [
                                str(coin["rank"]),
                                asset_str,
                                f"${coin['price']:,.2f}",
                                change_str,
                                format_large_number(coin["mcap"]),
                                format_large_number(coin["vol"])
                            ]
                            table_rows.append(row)

                        MenuV2.draw_table(headers, table_rows, widths)
                        input(f"\n{ui_return_msg}")

                    elif action == "view_listings":
                        title = "YENİ LİSTELEMELER" if current_lang == "tr" else "NEW LISTINGS"
                        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

                        data = market_service.get_new_listings()

                        if current_lang == "tr":
                            headers = ["Sembol", "İsim", "Fiyat", "Perf", "Tarih"]
                        else:
                            headers = ["Symbol", "Name", "Price", "Perf", "Date"]

                        widths = [10, 15, 15, 15, 15]
                        table_rows = []

                        for coin in data:
                            row = [coin["symbol"], coin["name"], f"${coin['price']}", f"{coin['change']}%",
                                   coin["date"]]
                            table_rows.append(row)

                        MenuV2.draw_table(headers, table_rows, widths)
                        input(f"\n{ui_return_msg}")

                    elif action == "view_gainers":
                        title = "KAZANANLAR & KAYBEDENLER" if current_lang == "tr" else "GAINERS & LOSERS"
                        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)
                        gainers, losers = market_service.get_gainers_losers()

                        t_gainers = "EN ÇOK KAZANANLAR" if current_lang == "tr" else "ROCKET GAINERS"
                        t_losers = "EN ÇOK KAYBEDENLER" if current_lang == "tr" else "TOP LOSERS"

                        print(f"   {C.GREEN}🚀 {t_gainers}{C.END}")
                        for g in gainers:
                            print(f"   • {g['symbol']:<10} {C.GREEN}+{g['change']}%{C.END} (${g['price']})")

                        print(f"\n   {C.FAIL}📉 {t_losers}{C.END}")
                        for l in losers:
                            print(f"   • {l['symbol']:<10} {C.FAIL}{l['change']}%{C.END} (${l['price']})")

                        input(f"\n\n{ui_return_msg}")

                    elif action == "view_sectors":
                        title = "SEKTÖR PERFORMANSI" if current_lang == "tr" else "SECTOR PERFORMANCE"
                        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

                        sectors = market_service.get_sector_data(current_lang)

                        if current_lang == "tr":
                            headers = ["#", "SEKTÖR", "PERF (24S)", "P. DEĞERİ", "LİDER COIN"]
                        else:
                            headers = ["#", "SECTOR", "PERF (24H)", "M. CAP", "TOP TOKEN"]

                        widths = [4, 22, 12, 12, 12]
                        table_rows = []

                        for s in sectors:
                            arrow = "▲" if s['perf'] >= 0 else "▼"
                            perf_str = f"{arrow} {s['perf']}%"

                            row = [
                                str(s['rank']),
                                s['name'],
                                perf_str,
                                s['mcap'],
                                s['top']
                            ]
                            table_rows.append(row)

                        MenuV2.draw_table(headers, table_rows, widths)
                        input(f"\n{ui_return_msg}")

                    # Fear and Greed Index
                    elif action == "view_fear_greed":
                        t_title = "KORKU & AÇGÖZLÜLÜK ENDEKSİ" if current_lang == "tr" else "FEAR & GREED INDEX"
                        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

                        fng_data = market_service.get_fear_greed_data(current_lang)
                        MenuV2.draw_gauge(fng_data["current_value"], fng_data["current_status"])

                        # Balance visual weight for alignment
                        if current_lang == "tr":
                            h_val = f"{C.CYAN}DEĞER{C.END}"
                            headers = ["DÖNEM", h_val, "DURUM"]
                        else:
                            h_val = f"{C.CYAN}VALUE{C.END}"
                            headers = ["PERIOD", h_val, "STATUS"]

                        widths = [15, 20, 25]
                        table_rows = []

                        for item in fng_data["history"]:
                            val = item['value']
                            # Color coding logic
                            if val < 45:
                                val_str = f"{C.FAIL}{val}{C.END}"
                            elif val > 55:
                                val_str = f"{C.GREEN}{val}{C.END}"
                            else:
                                val_str = f"{C.CYAN}{val}{C.END}"

                            table_rows.append([
                                item['period'],
                                val_str,
                                item['status']
                            ])

                        MenuV2.draw_table(headers, table_rows, widths)
                        input(f"\n{ui_return_msg}")

                    # Analysis tools
                    elif action == "show_chart":
                        t_title = "TRADINGVIEW GRAFİK" if current_lang == "tr" else "TRADINGVIEW CHART"
                        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

                        # 1. Fetch assets
                        assets = market_service.get_all_assets()

                        # 2. Draw selection menu (Pass current_lang for localization)
                        MenuV2.draw_asset_selector(assets, current_lang)

                        # 3. Input prompt
                        p_msg = "Varlık Numarası Seçin (0-7): " if current_lang == "tr" else "Select Asset Number (0-7): "
                        print(f"{ui_input_prefix}{p_msg}", end="")

                        choice = input().strip()

                        # 4. Validation
                        if not choice.isdigit():
                            err_msg = "Geçersiz giriş!" if current_lang == "tr" else "Invalid input!"
                            print(f"\n   {C.FAIL}{err_msg}{C.END}")
                            time.sleep(1)
                            continue

                        choice_idx = int(choice)

                        # 5. Cancel logic
                        if choice_idx == 0:
                            continue

                        # 6. Selection logic
                        if 1 <= choice_idx <= len(assets):
                            # Adjust index since list starts at 1
                            selected_asset = assets[choice_idx - 1]
                            target_symbol = selected_asset['symbol']

                            # Loading effect
                            load_msg = "Veriler yükleniyor..." if current_lang == "tr" else "Loading chart data..."
                            print(f"\n   {C.WARNING}{load_msg}{C.END}")
                            time.sleep(0.5)

                            # Fetch and draw chart
                            chart_data = market_service.get_chart_data(target_symbol)
                            MenuV2.draw_simple_chart(target_symbol, chart_data)

                            input(f"{ui_return_msg}")
                        else:
                            # Out of range error
                            err_msg = "Varlık bulunamadı!" if current_lang == "tr" else "Asset not found!"
                            print(f"\n   {C.FAIL}{err_msg}{C.END}")
                            time.sleep(1)

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