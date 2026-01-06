from ui.menu import Menu
from ui.strings import STRINGS


def main():
    aktif_dil = "tr"  # Varsayılan dil

    while True:
        Menu.misafir_paneli_ciz(aktif_dil)
        secim = input(STRINGS[aktif_dil]["choice"]).upper()

        if secim == "1":
            Menu.mesaj_goster("Piyasalar cok yakinda burada olacak...")
            input("\nDevam...")
        elif secim == "4":
            aktif_dil = "en" if aktif_dil == "tr" else "tr"
        elif secim == "Q":
            print(STRINGS[aktif_dil]["logout"])
            break
        elif secim == "L":
            Menu.mesaj_goster("Giris ekrani hazirlaniyor...")
            input("\nDevam...")
        else:
            input(STRINGS[aktif_dil]["invalid"])


if __name__ == "__main__":
    main()