import os
from ui.strings import STRINGS


class Menu:
    @staticmethod
    def clear_screen():
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def draw_guest_dashboard(language):
        """Renders the dashboard for unauthenticated users."""
        s = STRINGS[language]
        Menu.clear_screen()

        # UI Frame
        print("=" * 74)
        print(f"   {s['app_title']}")
        print("=" * 74)
        print(f" {s['menu_header_left']:<34} |  {s['menu_header_right']}")
        print("-" * 35 + " | " + "-" * 36)
        print(f" {s['m_markets']:<34} |  {s['m_login']}")
        print(f" {s['m_news']:<34} |  {s['m_register']}")
        print(f" {s['m_support']:<34} |  ")
        print(f" {s['m_lang']:<34} |  {s['m_exit']}")
        print("-" * 35 + " | " + "-" * 36)

    @staticmethod
    def show_message(text):
        """Displays a system message to the user."""
        print(f"\n[!] {text}")