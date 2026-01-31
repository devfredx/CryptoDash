class NewsService:
    """Provides latest crypto news based on selected language."""

    def __init__(self):
        # Haber veri tabanı: Dil koduna göre listeler
        self.news_data = {
            "tr": [
                {"date": "2026-01-31", "source": "CoinDesk TR", "title": "Bitcoin 100.000$ barajini zorluyor! Uzmanlar ne diyor?"},
                {"date": "2026-01-30", "source": "Bloomberg HT", "title": "Ethereum 2.0 guncellemesi tamamlandi: Gaz ucretleri dustu."},
                {"date": "2026-01-29", "source": "KriptoBulten", "title": "Elon Musk'tan yeni DOGE paylasimi: Piyasa hareketlendi."},
                {"date": "2026-01-28", "source": "Webrazzi", "title": "Dev bankalar kripto saklama hizmeti vermeye basliyor."},
                {"date": "2026-01-27", "source": "DonanimHaber", "title": "Metaverse arsa fiyatlarinda buyuk dusus: Balon patladi mi?"}
            ],
            "en": [
                {"date": "2026-01-31", "source": "CoinDesk", "title": "Bitcoin touches $100k resistance! Analysts are bullish."},
                {"date": "2026-01-30", "source": "Bloomberg", "title": "Ethereum 2.0 update finalized: Gas fees are dropping."},
                {"date": "2026-01-29", "source": "CryptoDaily", "title": "New DOGE tweet from Elon Musk: Market is moving fast."},
                {"date": "2026-01-28", "source": "TechCrunch", "title": "Major banks start offering crypto custody services."},
                {"date": "2026-01-27", "source": "Investopedia", "title": "Massive drop in Metaverse land prices: Is the bubble bursting?"}
            ]
        }

    def get_latest_news(self, language="tr"):
        """Returns news articles based on the language code."""
        # İstenen dili getir, yoksa varsayılan olarak Türkçe getir
        return self.news_data.get(language, self.news_data["tr"])