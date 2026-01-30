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

    @staticmethod
    def draw_member_dashboard(language, user):
        """Renders the dashboard for logged-in members."""
        s = STRINGS[language]
        Menu.clear_screen()

        # Header with User Info
        print("=" * 74)
        header_text = f"   CryptoDash PRO | {user.username.upper()} | {user.balance} USDT"
        print(f"{header_text:<74}")
        print("=" * 74)

        # Member Menu Options (DÜZELTİLMİŞ SIRALAMA)
        print(f" {s['menu_header_left']:<34} |  {s['menu_header_right']}")
        print("-" * 35 + " | " + "-" * 36)

        # Satır 1: Piyasalar (1) ve Cüzdan (2)
        print(f" {s['m_markets']:<34} |  {s['m_wallet']}")

        # Satır 2: Al-Sat (3) ve Haberler (4)
        print(f" {s['m_trade']:<34} |  {s['m_news']}")

        # Satır 3: Geçmiş (5) ve Ayarlar (6)
        print(f" {s['m_history']:<34} |  {s['m_settings']}")

        # Satır 4: Destek (D) ve Çıkış (O)
        print(f" {s['m_support']:<34} |  {s['m_logout']}")

        print("-" * 35 + " | " + "-" * 36)

    @staticmethod
    def show_market_table(assets):
        """Displays assets in a formatted table."""
        Menu.clear_screen()
        print("=" * 40)
        print(f" {'SYMBOL':<10} | {'PRICE (USDT)':<15}")
        print("-" * 40)

        for asset in assets:
            print(f" {asset.symbol:<10} | ${asset.current_price:<15,.2f}")

        print("=" * 40)

    @staticmethod
    def show_wallet_details(summary):
        """Displays detailed wallet portfolio."""
        Menu.clear_screen()
        print("=" * 50)
        print(f"            MY WALLET SUMMARY")
        print("=" * 50)

        # 1. Nakit Bakiye
        print(f" CASH BALANCE   : ${summary['balance_usdt']:,.2f}")

        # 2. Varlıklar
        print("-" * 50)
        print(f" {'ASSET':<10} {'AMOUNT':<10} {'PRICE':<12} {'VALUE':<12}")
        print("-" * 50)

        if not summary['assets']:
            print("  No crypto assets yet.")
        else:
            for item in summary['assets']:
                print(
                    f" {item['symbol']:<10} {item['amount']:<10.4f} ${item['price']:<11,.0f} ${item['total_value']:<11,.2f}")

        # 3. Toplam Servet
        print("-" * 50)
        print(f" TOTAL WEALTH   : ${summary['total_wealth']:,.2f}")
        print("=" * 50)

    @staticmethod
    def draw_trade_menu():
        """Displays options for buying or selling."""
        Menu.clear_screen()
        print("=" * 40)
        print("          TRADE OPERATIONS")
        print("=" * 40)
        print(" [B] BUY COIN  (USDT -> COIN)")
        print(" [S] SELL COIN (COIN -> USDT)")
        print(" [X] BACK TO MENU")
        print("-" * 40)

    @staticmethod
    def show_history(history):
        """Displays transaction history table."""
        Menu.clear_screen()
        print("=" * 65)
        print("          TRANSACTION HISTORY")
        print("=" * 65)
        print(f" {'DATE':<18} {'TYPE':<6} {'SYMBOL':<8} {'AMOUNT':<10} {'PRICE':<10}")
        print("-" * 65)

        if not history:
            print("  No transactions found.")
        else:
            # En son işlem en üstte görünsün diye ters çeviriyoruz (reversed)
            for item in reversed(history):
                print(
                    f" {item['date']:<18} {item['type']:<6} {item['symbol']:<8} {item['amount']:<10.4f} ${item['price']:<10,.0f}")

        print("=" * 65)