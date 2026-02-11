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
        # Simple header
        print(f"\n 📍 CRYPTODASH > {path_str}")
        print("-" * 120)
        # User info is now dynamic
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
        # Header title is now dynamic
        MenuV2.draw_header(page_title, user_info)

        col_width = 20
        header_row = ""
        separator_row = ""

        for key, val in menu_tree.items():
            # Color the number only
            title = f"{C.WARNING}{key}.{C.END} {val['title']}"

            # Calculate padding
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
        # Footer text is now dynamic
        print(f" {footer_text}")

    @staticmethod
    def draw_submenu(menu_data, breadcrumb_path, user_info):
        MenuV2.clear_screen()
        path_str = " > ".join(breadcrumb_path)
        MenuV2.draw_header(path_str, user_info)

        print(f"   --- {menu_data['title']} ---\n")

        for key, val in menu_data['options'].items():
            # Color logic for buttons
            if val['action'] == "GO_BACK":
                print(f"   [{C.FAIL}{key}{C.END}] {val['label']}")
            else:
                print(f"   [{C.WARNING}{key}{C.END}] {val['label']}")

        print("")

    @staticmethod
    def draw_table(headers, data, col_widths):
        """
        Generic table drawer with modern alignment.
        Supports automatic color coding for price changes.
        """

        # 1. Draw header row
        header_str = "   "
        for i, h in enumerate(headers):
            # Headers are bold and cyan
            header_str += f"{C.BOLD}{C.CYAN}{h:<{col_widths[i]}}{C.END}"

        print(header_str)
        # Separator line
        print("   " + f"{C.GREY}{'─' * (sum(col_widths))}{C.END}")

        # 2. Draw data rows
        for row in data:
            row_str = "   "
            for i, item in enumerate(row):
                val_str = str(item)
                color = C.END

                # Logic for coloring percentages and arrows
                if "%" in val_str:
                    if "-" in val_str or "▼" in val_str:
                        color = C.FAIL  # Red
                    else:
                        color = C.GREEN  # Green

                # Highlight rank number in orange
                if i == 0 and val_str.isdigit():
                    color = C.WARNING

                row_str += f"{color}{val_str:<{col_widths[i]}}{C.END}"
            print(row_str)

        # 3. Bottom border
        print("   " + f"{C.GREY}{'─' * (sum(col_widths))}{C.END}")
        print("")

    @staticmethod
    def draw_gauge(value, label, width=50):
        """
        Draws a visual progress bar (gauge) for 0-100 values.
        """
        # Determine color based on value
        color = C.GREY
        if value < 25:
            color = C.FAIL  # Red
        elif value < 45:
            color = C.WARNING  # Orange
        elif value < 55:
            color = C.CYAN  # Blue
        else:
            color = C.GREEN  # Green

        # Calculate filled portion
        filled_len = int(width * value // 100)
        bar = '█' * filled_len + '-' * (width - filled_len)

        print(f"\n   {C.BOLD}MARKET SENTIMENT: {color}{label.upper()}{C.END}")
        print(f"   {color}[{bar}] {value}/100{C.END}\n")

    @staticmethod
    def draw_simple_chart(symbol, prices):
        """
        Draws a simple horizontal bar chart for price history.
        """
        if not prices:
            print("No data available.")
            return

        print(f"\n   {C.BOLD}{symbol} Price Action (Last 20){C.END}")
        print(f"   {C.GREY}{'-' * 40}{C.END}")

        min_p = min(prices)
        max_p = max(prices)
        diff = max_p - min_p

        if diff == 0: diff = 1

        for price in prices:
            # Simple scaling logic
            length = int((price - min_p) / diff * 30)
            bar = "█" * length
            if length == 0: bar = "▏"

            print(f"   ${price:,.2f} | {C.CYAN}{bar}{C.END}")

        print("")

    @staticmethod
    def draw_asset_selector(assets, lang="en"):
        """
        Displays a numbered list of assets for user selection.
        """
        # Localize headers based on lang param
        if lang == "tr":
            title = "MEVCUT VARLIKLAR"
            txt_cancel = "İptal"
        else:
            title = "AVAILABLE ASSETS"
            txt_cancel = "Cancel"

        print(f"\n   {C.BOLD}{title}{C.END}")
        print(f"   {C.GREY}{'-' * 40}{C.END}")

        for i, asset in enumerate(assets, 1):
            # Format: [1] BTC • Bitcoin
            row = f"   [{C.WARNING}{i}{C.END}] {C.CYAN}{asset['symbol']}{C.END} • {asset['name']}"
            print(row)

        # Add Cancel/Back option
        print(f"   [{C.FAIL}0{C.END}] {txt_cancel}")
        print("")

    @staticmethod
    def draw_heatmap(data, lang="en"):
        """
        draws a 3x3 grid of boxes with color coded performance
        """
        if not data: return

        # Localization Logic
        if lang == "tr":
            title = "PİYASA ISI HARİTASI (İLK 9)"
        else:
            title = "MARKET HEATMAP (TOP 9)"

        print(f"\n   {C.BOLD}{title}{C.END}")

        # split data into chunks of 3 for rows
        rows = [data[i:i + 3] for i in range(0, len(data), 3)]

        border = "+-------------+   "

        for row_items in rows:
            # top borders
            print(f"   {border * len(row_items)}")

            # symbol row
            line_sym = "   "
            for item in row_items:
                sym = item['symbol']
                line_sym += f"| {C.BOLD}{sym:<11}{C.END} |   "
            print(line_sym)

            # percent row
            line_pct = "   "
            for item in row_items:
                chg = item['change']

                # determine color
                if chg > 0:
                    color = C.GREEN
                elif chg < 0:
                    color = C.FAIL
                else:
                    color = C.GREY

                pct_str = f"{chg:+.2f}%"
                line_pct += f"| {color}{pct_str:^11}{C.END} |   "
            print(line_pct)

            # bottom borders
            print(f"   {border * len(row_items)}")
        print("")