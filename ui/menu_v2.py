# ui/menu_v2.py

import os
import sys


# ANSI color codes
class C:
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'
    GREY = '\033[90m'
    BOLD = '\033[1m'


class MenuV2:
    @staticmethod
    def clear_screen():
        # Clear terminal screen based on OS
        os.system('cls' if os.name == 'nt' else 'clear')
        # ANSI escape code for IDE support
        sys.stdout.write("\033[H\033[J")

    @staticmethod
    def draw_header(path_str, user_info):
        # Print simple header
        print(f"\n 📍 CRYPTODASH > {path_str}")
        print("-" * 120)
        # Display dynamic user info
        print(f" 👤 {user_info:<90} 🌐 v2.0-dev")
        print("")

    @staticmethod
    def prepare_content_screen(breadcrumb_path, user_info):
        MenuV2.clear_screen()
        path_str = " > ".join(breadcrumb_path)
        MenuV2.draw_header(path_str, user_info)

    @staticmethod
    def draw_mega_dashboard(menu_tree, page_title="HOME", user_info="Guest", footer_text="[Select Column: 1-6]"):
        MenuV2.clear_screen()
        MenuV2.draw_header(page_title, user_info)

        # Set column width back to 20 for compact view
        col_width = 20
        header_row = ""
        separator_row = ""

        for key, val in menu_tree.items():
            # Color the number only
            title = f"{C.WARNING}{key}.{C.END} {val['title']}"

            # Calculate padding based on width
            visible_len = len(f"{key}. {val['title']}")
            padding = " " * (col_width - visible_len)

            header_row += f"{title}{padding}"
            separator_row += f"{'-' * 15:<{col_width}}"

        print(f" {header_row}")
        print(f" {separator_row}")

        max_rows = 0
        for val in menu_tree.values():
            if len(val['preview']) > max_rows:
                max_rows = len(val['preview'])

        for i in range(max_rows):
            row_str = ""
            for key, val in menu_tree.items():
                items = val['preview']
                if i < len(items):
                    item_text = f"• {items[i]}"
                    row_str += f"{item_text:<{col_width}}"
                else:
                    row_str += f"{' ':<{col_width}}"

            print(f" {row_str}")

        print("\n" + "=" * 120)
        print(f" {footer_text}")

    @staticmethod
    def draw_submenu(menu_data, breadcrumb_path, user_info):
        MenuV2.clear_screen()
        path_str = " > ".join(breadcrumb_path)
        MenuV2.draw_header(path_str, user_info)

        print(f"   --- {menu_data['title']} ---\n")

        for key, val in menu_data['options'].items():
            if val['action'] == "GO_BACK":
                print(f"   [{C.FAIL}{key}{C.END}] {val['label']}")
            else:
                print(f"   [{C.WARNING}{key}{C.END}] {val['label']}")
        print("")

    @staticmethod
    def draw_table(headers, data, col_widths):
        # Draw generic table with flexible column widths
        header_str = "   "
        for i, h in enumerate(headers):
            header_str += f"{C.BOLD}{C.CYAN}{h:<{col_widths[i]}}{C.END}"

        print(header_str)
        print("   " + f"{C.GREY}{'─' * (sum(col_widths))}{C.END}")

        for row in data:
            row_str = "   "
            for i, item in enumerate(row):
                val_str = str(item)
                color = C.END
                if "%" in val_str:
                    if "-" in val_str or "▼" in val_str:
                        color = C.FAIL
                    else:
                        color = C.GREEN
                if i == 0 and val_str.isdigit():
                    color = C.WARNING

                row_str += f"{color}{val_str:<{col_widths[i]}}{C.END}"
            print(row_str)

        print("   " + f"{C.GREY}{'─' * (sum(col_widths))}{C.END}")
        print("")

    @staticmethod
    def draw_gauge(value, label, title="MARKET SENTIMENT", width=50):
        # calculate gauge color based on value
        color = C.GREY
        if value < 25:
            color = C.FAIL
        elif value < 45:
            color = C.WARNING
        elif value < 55:
            color = C.CYAN
        else:
            color = C.GREEN

        filled_len = int(width * value // 100)
        bar = '█' * filled_len + '-' * (width - filled_len)

        # print gauge with dynamic title to allow localization
        print(f"\n   {C.BOLD}{title}: {color}{label.upper()}{C.END}")
        print(f"   {color}[{bar}] {value}/100{C.END}\n")

    @staticmethod
    def draw_asset_selector(assets, lang="en"):
        if lang == "tr":
            title = "MEVCUT VARLIKLAR"
            txt_cancel = "İptal"
        else:
            title = "AVAILABLE ASSETS"
            txt_cancel = "Cancel"

        print(f"\n   {C.BOLD}{title}{C.END}")
        print(f"   {C.GREY}{'-' * 40}{C.END}")

        for i, asset in enumerate(assets, 1):
            row = f"   [{C.WARNING}{i}{C.END}] {C.CYAN}{asset['symbol']}{C.END} • {asset['name']}"
            print(row)

        print(f"   [{C.FAIL}0{C.END}] {txt_cancel}")
        print("")

    @staticmethod
    def draw_simple_chart(symbol, prices, lang="en"):
        # check if price data exists
        if not prices:
            msg = "Veri bulunamadı" if lang == "tr" else "No data available"
            print(f"   {msg}")
            return

        # define localized chart header
        header = f"{symbol} Fiyat Hareketi (Son 20)" if lang == "tr" else f"{symbol} Price Action (Last 20)"
        print(f"\n   {C.BOLD}{header}{C.END}")
        print(f"   {C.GREY}{'-' * 40}{C.END}")

        min_p = min(prices)
        max_p = max(prices)
        diff = max_p - min_p

        if diff == 0: diff = 1

        # render each price bar with manual alignment
        for price in prices:
            length = int((price - min_p) / diff * 30)
            bar = "█" * length
            if length == 0: bar = "▏"
            print(f"   ${price:,.2f} | {C.CYAN}{bar}{C.END}")
        print("")

    @staticmethod
    def draw_heatmap(data, lang="en"):
        if not data: return

        if lang == "tr":
            title = "PİYASA ISI HARİTASI (İLK 9)"
        else:
            title = "MARKET HEATMAP (TOP 9)"

        print(f"\n   {C.BOLD}{title}{C.END}")

        rows = [data[i:i + 3] for i in range(0, len(data), 3)]
        border = "+-------------+   "

        for row_items in rows:
            print(f"   {border * len(row_items)}")
            line_sym = "   "
            for item in row_items:
                sym = item['symbol']
                line_sym += f"| {C.BOLD}{sym:<11}{C.END} |   "
            print(line_sym)

            line_pct = "   "
            for item in row_items:
                chg = item['change']
                if chg > 0:
                    color = C.GREEN
                elif chg < 0:
                    color = C.FAIL
                else:
                    color = C.GREY
                pct_str = f"{chg:+.2f}%"
                line_pct += f"| {color}{pct_str:^11}{C.END} |   "
            print(line_pct)
            print(f"   {border * len(row_items)}")
        print("")

    @staticmethod
    def draw_onchain_report(data, lang="en"):
        # render detailed on chain analysis report
        if not data: return

        lbl = data['labels']
        sym = data['symbol']

        # define localized report header
        header = "ZİNCİR ÜSTÜ ANALİZ" if lang == "tr" else "ON-CHAIN ANALYSIS"
        print(f"\n   {C.BOLD}{header}: {C.WARNING}{sym}{C.END}")
        print(f"   {C.GREY}{'-' * 50}{C.END}")

        total_vol = data['inflow'] + data['outflow']
        if total_vol == 0: total_vol = 1

        pct_in = int((data['inflow'] / total_vol) * 20)
        pct_out = int((data['outflow'] / total_vol) * 20)

        bar_in = f"{C.FAIL}{'<' * pct_in}{C.END}"
        bar_out = f"{C.GREEN}{'>' * pct_out}{C.END}"

        print(f"\n   {C.BOLD}{lbl['net'].upper()}{C.END}")
        print(f"   {lbl['in']}: {C.FAIL}${data['inflow']:,.0f}{C.END}")
        print(f"   {lbl['out']}: {C.GREEN}${data['outflow']:,.0f}{C.END}")

        print(f"   [{bar_in:^25}|{bar_out:^25}]")

        sig_color = C.GREEN if data['net_flow'] > 0 else C.FAIL
        print(f"   SIGNAL: {sig_color}{data['signal']}{C.END}\n")

        print(f"   {C.GREY}{'-' * 50}{C.END}")

        print(f"   {lbl['addr']}: {C.CYAN}{data['active_addresses']:,}{C.END}")
        print(f"   {lbl['whale']}:  {C.WARNING}{data['whale_conc']:.1f}%{C.END}")
        print("")