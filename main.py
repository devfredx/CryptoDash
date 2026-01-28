from ui.menu import Menu
from ui.strings import STRINGS
from repository.user_repository import UserRepository
from service.auth_service import AuthService


def main():
    # 1. Initialize Architecture
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    # 2. Application State
    current_lang = "tr"
    current_session = None  # None = Misafir, User Object = Üye Giriş Yaptı

    while True:
        s = STRINGS[current_lang]

        # --- DURUM 1: MİSAFİR MODU (Giriş Yapılmamış) ---
        if current_session is None:
            Menu.draw_guest_dashboard(current_lang)
            choice = input(s["choice"]).upper()

            if choice == "R":
                # Register Logic
                Menu.clear_screen()
                print(f"--- {s['m_register'].upper()} ---")
                u_name = input(f"{s['choice']} (Username): ")
                p_word = input(f"{s['choice']} (Password): ")
                success, msg = auth_service.register(u_name, p_word)
                Menu.show_message(msg)
                input("\nPress Enter...")

            elif choice == "L":
                # LOGIN LOGIC (BURASI EKLENDİ)
                Menu.clear_screen()
                print(f"--- {s['m_login'].upper()} ---")
                u_name = input(f"{s['choice']} (Username): ")
                p_word = input(f"{s['choice']} (Password): ")

                # Servise sor: Bu bilgiler doğru mu?
                user = auth_service.login(u_name, p_word)

                if user:
                    current_session = user  # OTURUM AÇILDI!
                    Menu.show_message(s["login_success"])
                else:
                    Menu.show_message(s["login_fail"])
                input("\nPress Enter...")

            elif choice == "4":
                current_lang = "en" if current_lang == "tr" else "tr"
            elif choice == "Q":
                print(s["logout"])
                break
            else:
                Menu.show_message("Please login or register first.")
                input("\nPress Enter...")

        # --- DURUM 2: ÜYE MODU (Giriş Yapılmış) ---
        else:
            # Artık Üye Panelini çiziyoruz
            Menu.draw_member_dashboard(current_lang, current_session)
            choice = input(s["choice"]).upper()

            if choice == "O":  # Logout
                current_session = None  # Oturumu kapat, Misafir moda dön
                Menu.show_message(s["logout"])
                input("\nPress Enter...")

            elif choice == "2":  # Wallet (Örnek)
                Menu.show_message(f"Wallet Balance: {current_session.balance} USDT")
                input("\nPress Enter...")

            else:
                Menu.show_message("Feature coming soon...")
                input("\nPress Enter...")


if __name__ == "__main__":
    main()