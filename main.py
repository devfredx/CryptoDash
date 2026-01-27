from ui.menu import Menu
from ui.strings import STRINGS
from repository.user_repository import UserRepository
from service.auth_service import AuthService


def main():
    # Initialize the architecture layers
    user_repo = UserRepository()
    auth_service = AuthService(user_repo)

    # Application state
    current_lang = "tr"

    while True:
        s = STRINGS[current_lang]
        Menu.draw_guest_dashboard(current_lang)
        choice = input(s["choice"]).upper()

        if choice == "1":
            Menu.show_message("Market details coming soon...")
            input("\nPress Enter...")

        elif choice == "4":
            current_lang = "en" if current_lang == "tr" else "tr"

        elif choice == "R":
            Menu.clear_screen()
            print(f"--- {s['m_register'].upper()} ---")
            u_name = input(f"{s['choice']} (Username): ")
            p_word = input(f"{s['choice']} (Password): ")

            success, message = auth_service.register(u_name, p_word)

            if success:
                Menu.show_message(f"{message} (User: {u_name})")
            else:
                Menu.show_message(f"ERROR: {message}")
            input("\nPress Enter...")

        elif choice == "Q":
            print(s["logout"])
            break

        else:
            input(s["invalid"])


if __name__ == "__main__":
    main()