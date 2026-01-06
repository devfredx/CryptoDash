import os
from ui.strings import STRINGS

class Menu:
    @staticmethod
    def temizle():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def misafir_paneli_ciz(dil):
        s = STRINGS[dil]
        Menu.temizle()
        print("=" * 72)
        print(f"   {s['app_title']}")
        print("=" * 72)
        print(f" {s['menu_header_left']:<33} |  {s['menu_header_right']}")
        print("-" * 34 + " | " + "-" * 35)
        print(f" {s['m_markets']:<33} |  {s['m_login']}")
        print(f" {s['m_news']:<33} |  {s['m_register']}")
        print(f" {s['m_support']:<33} |  ")
        print(f" {s['m_lang']:<33} |  {s['m_exit']}")
        print("-" * 34 + " | " + "-" * 35)

    @staticmethod
    def mesaj_goster(metin):
        print(f"\n[!] {metin}")