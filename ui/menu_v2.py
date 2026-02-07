# ui/menu_v2.py

import os
import sys


# ansi color codes
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
        # clear terminal screen based on os
        os.system('cls' if os.name == 'nt' else 'clear')
        # ansi escape code for ide support
        sys.stdout.write("\033[H\033[J")

    @staticmethod
    def draw_header(path_str, user_info):
        # simple header
        print(f"\n 📍 CRYPTODASH > {path_str}")
        print("-" * 120)
        # user_info is now dynamic (Guest or Misafir)
        print(f" 👤 {user_info:<90} 🌐 v2.0-dev")
        print("")

    @staticmethod
    def prepare_content_screen(breadcrumb_path, user_info):
        MenuV2.clear_screen()
        path_str = " > ".join(breadcrumb_path)
        MenuV2.draw_header(path_str, user_info)

    @staticmethod
    def draw_mega_dashboard(menu_tree, page_title="HOME", user_info="Guest"):
        MenuV2.clear_screen()
        # Header title is now dynamic
        MenuV2.draw_header(page_title, user_info)

        col_width = 20
        header_row = ""
        separator_row = ""

        for key, val in menu_tree.items():
            # color the number only
            title = f"{C.WARNING}{key}.{C.END} {val['title']}"

            # calculate padding
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
        print(" [Select Column: 1-6]")

    @staticmethod
    def draw_submenu(menu_data, breadcrumb_path, user_info):
        MenuV2.clear_screen()
        path_str = " > ".join(breadcrumb_path)
        MenuV2.draw_header(path_str, user_info)

        print(f"   --- {menu_data['title']} ---\n")

        for key, val in menu_data['options'].items():
            # color logic for buttons
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

        # 1. draw header row with cyan color
        header_str = "   "
        for i, h in enumerate(headers):
            # headers are bold and cyan
            header_str += f"{C.BOLD}{C.CYAN}{h:<{col_widths[i]}}{C.END}"

        print(header_str)
        # modern thin separator line
        print("   " + f"{C.GREY}{'─' * (sum(col_widths))}{C.END}")

        # 2. draw data rows
        for row in data:
            row_str = "   "
            for i, item in enumerate(row):
                val_str = str(item)
                color = C.END

                # logic for coloring percentages and arrows
                if "%" in val_str:
                    if "-" in val_str or "▼" in val_str:
                        color = C.FAIL  # red
                    else:
                        color = C.GREEN  # green

                # highlight rank number in orange
                if i == 0 and val_str.isdigit():
                    color = C.WARNING

                row_str += f"{color}{val_str:<{col_widths[i]}}{C.END}"
            print(row_str)

        # 3. bottom border
        print("   " + f"{C.GREY}{'─' * (sum(col_widths))}{C.END}")
        print("")