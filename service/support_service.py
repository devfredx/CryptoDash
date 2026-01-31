class SupportService:
    """Provides FAQ content and contact information."""

    def __init__(self):
        self.support_data = {
            "tr": {
                "contact": {"email": "destek@cryptodash.com", "phone": "+90 (212) 555 00 00"},
                "faqs": [
                    {"q": "Nasil kayit olurum?", "a": "Ana menude 'R' tusuna basarak kullanici adi ve sifre belirleyebilirsiniz."},
                    {"q": "Bakiye nasil yuklenir?", "a": "Sistem otomatik olarak her yeni kullaniciya 10.000 USDT tanimlar."},
                    {"q": "Islem gecmisimi nerede gorebilirim?", "a": "Giris yaptiktan sonra '5' tusuna basarak tum islemlerinizi listeleyebilirsiniz."},
                    {"q": "Sifremi unuttum, ne yapmaliyim?", "a": "Sifre sifirlama islemi icin destek ekibimize mail atabilirsiniz."}
                ]
            },
            "en": {
                "contact": {"email": "support@cryptodash.com", "phone": "+44 20 7946 0000"},
                "faqs": [
                    {"q": "How can I register?", "a": "Press 'R' in the main menu to set up your username and password."},
                    {"q": "How to deposit funds?", "a": "The system automatically grants 10,000 USDT to every new user."},
                    {"q": "Where is my history?", "a": "After login, press '5' to view all your past transactions."},
                    {"q": "I forgot my password.", "a": "Please contact our support team via email for password recovery."}
                ]
            }
        }

    def get_support_content(self, language="tr"):
        return self.support_data.get(language, self.support_data["tr"])