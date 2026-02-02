# ui/menu_v2.py

import os


class MenuV2:
    @staticmethod
    def clear_screen():
        # clear terminal screen based on os
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def draw_header(path_str, user_info="Guest"):
        # simple header without heavy borders
        print(f"\n 📍 CRYPTODASH > {path_str}")
        print("-" * 120)  # thin separator line
        print(f" 👤 {user_info:<90} 🌐 v2.0-dev")
        print("")  # empty line for spacing

    @staticmethod
    def draw_mega_dashboard(menu_tree):
        MenuV2.clear_screen()
        MenuV2.draw_header("ANA SAYFA")

        # set column width for alignment
        col_width = 19

        header_row = ""
        separator_row = ""

        # build header rows from menu keys
        for key, val in menu_tree.items():
            title = f"{key}. {val['title']}"
            header_row += f"{title:<{col_width}}"
            separator_row += f"{'-' * 15:<{col_width}}"

        print(f" {header_row}")
        print(f" {separator_row}")

        # find max rows needed for columns
        max_rows = 0
        for val in menu_tree.values():
            if len(val['preview']) > max_rows:
                max_rows = len(val['preview'])

        # print items row by row
        for i in range(max_rows):
            row_str = ""
            for key, val in menu_tree.items():
                items = val['preview']

                # check if item exists at this index
                if i < len(items):
                    item_text = f"• {items[i]}"
                    row_str += f"{item_text:<{col_width}}"
                else:
                    row_str += f"{' ':<{col_width}}"

            print(f" {row_str}")

        # simple footer prompt
        print("\n" + "=" * 120)
        print("\n [Select Column: 1-6]")

    @staticmethod
    def draw_submenu(menu_data, breadcrumb_path):
        MenuV2.clear_screen()

        # join path elements for display
        path_str = " > ".join(breadcrumb_path)
        MenuV2.draw_header(path_str)

        print(f"   --- {menu_data['title']} ---\n")

        # list all options
        for key, val in menu_data['options'].items():
            print(f"   [{key}] {val['label']}")

        print("")  # bottom spacing