# service/market_service.py

class MarketService:
    def __init__(self):
        # mock database with extended market data
        self.assets = [
            {"rank": 1, "symbol": "BTC", "name": "Bitcoin", "price": 43250.0, "change": 2.4, "vol": 35000000000,
             "mcap": 845000000000},
            {"rank": 2, "symbol": "ETH", "name": "Ethereum", "price": 2340.5, "change": -1.2, "vol": 15000000000,
             "mcap": 278000000000},
            {"rank": 3, "symbol": "SOL", "name": "Solana", "price": 98.4, "change": 5.8, "vol": 4200000000,
             "mcap": 41000000000},
            {"rank": 4, "symbol": "BNB", "name": "Binance", "price": 315.0, "change": 0.5, "vol": 900000000,
             "mcap": 48000000000},
            {"rank": 5, "symbol": "XRP", "name": "Ripple", "price": 0.55, "change": -0.8, "vol": 1200000000,
             "mcap": 29000000000},
            {"rank": 6, "symbol": "ADA", "name": "Cardano", "price": 0.52, "change": -2.1, "vol": 450000000,
             "mcap": 18000000000},
            {"rank": 7, "symbol": "AVAX", "name": "Avalanche", "price": 36.8, "change": 8.4, "vol": 600000000,
             "mcap": 13500000000},
        ]

    def get_top_coins(self):
        return self.assets

    def get_new_listings(self):
        return [
            {"symbol": "PYTH", "name": "Pyth Network", "price": 0.45, "change": 150.0, "date": "2 Days Ago"},
            {"symbol": "TIA", "name": "Celestia", "price": 12.3, "change": 45.0, "date": "1 Week Ago"},
            {"symbol": "JUP", "name": "Jupiter", "price": 0.65, "change": -5.0, "date": "Just Now"},
        ]

    def get_gainers_losers(self):
        sorted_assets = sorted(self.assets, key=lambda x: x['change'], reverse=True)
        gainers = sorted_assets[:3]
        losers = sorted_assets[-3:]
        return gainers, losers

    def get_sector_data(self, lang="en"):
        # mock data with localization support
        if lang == "tr":
            return [
                {"rank": 1, "name": "Katman 1 (L1)", "perf": 1.2, "mcap": "1.4T", "top": "BTC"},
                {"rank": 2, "name": "Akıllı Sözleşmeler", "perf": -0.5, "mcap": "450B", "top": "ETH"},
                {"rank": 3, "name": "Yapay Zeka & Veri", "perf": 14.5, "mcap": "12B", "top": "TAO"},
                {"rank": 4, "name": "DeFi (Finans)", "perf": 2.1, "mcap": "65B", "top": "UNI"},
                {"rank": 5, "name": "Oyun / Metaverse", "perf": -3.2, "mcap": "18B", "top": "IMX"},
                {"rank": 6, "name": "Meme Coinler", "perf": 8.4, "mcap": "25B", "top": "DOGE"},
                {"rank": 7, "name": "Gerçek Varlıklar (RWA)", "perf": 0.8, "mcap": "5B", "top": "ONDO"},
            ]
        else:
            return [
                {"rank": 1, "name": "Layer 1", "perf": 1.2, "mcap": "1.4T", "top": "BTC"},
                {"rank": 2, "name": "Smart Contracts", "perf": -0.5, "mcap": "450B", "top": "ETH"},
                {"rank": 3, "name": "AI & Big Data", "perf": 14.5, "mcap": "12B", "top": "TAO"},
                {"rank": 4, "name": "DeFi (Finance)", "perf": 2.1, "mcap": "65B", "top": "UNI"},
                {"rank": 5, "name": "Gaming / Metaverse", "perf": -3.2, "mcap": "18B", "top": "IMX"},
                {"rank": 6, "name": "Meme Coins", "perf": 8.4, "mcap": "25B", "top": "DOGE"},
                {"rank": 7, "name": "RWA (Real World)", "perf": 0.8, "mcap": "5B", "top": "ONDO"},
            ]

    def get_all_assets(self):
        return self.assets

    def get_fear_greed_data(self, lang="en"):
        """
        returns mock fear and greed index data with localization
        """
        # score between 0 and 100
        current_score = 74

        # localization dictionary
        labels = {
            "en": {
                "extreme_fear": "Extreme Fear",
                "fear": "Fear",
                "neutral": "Neutral",
                "greed": "Greed",
                "extreme_greed": "Extreme Greed",
                "periods": ["Now", "Yesterday", "Last Week", "Last Month"]
            },
            "tr": {
                "extreme_fear": "Aşırı Korku",
                "fear": "Korku",
                "neutral": "Nötr",
                "greed": "Açgözlülük",
                "extreme_greed": "Aşırı Açgözlülük",
                "periods": ["Şimdi", "Dün", "Geçen Hafta", "Geçen Ay"]
            }
        }

        txt = labels.get(lang, labels["en"])

        # helper to determine status label based on score
        def get_status(score):
            if score < 25: return txt["extreme_fear"]
            if score < 45: return txt["fear"]
            if score < 55: return txt["neutral"]
            if score < 75: return txt["greed"]
            return txt["extreme_greed"]

        # mock historical data
        history = [
            {"period": txt["periods"][0], "value": current_score, "status": get_status(current_score)},
            {"period": txt["periods"][1], "value": 65, "status": txt["greed"]},
            {"period": txt["periods"][2], "value": 45, "status": txt["neutral"]},
            {"period": txt["periods"][3], "value": 20, "status": txt["extreme_fear"]},
        ]

        return {
            "current_value": current_score,
            "current_status": get_status(current_score),
            "history": history
        }

    def get_chart_data(self, symbol):
        """
        generates last 20 price data for simple chart
        """
        import random

        # set base price based on symbol
        base_price = 100.0
        if symbol == "BTC":
            base_price = 42500.0
        elif symbol == "ETH":
            base_price = 2300.0
        elif symbol == "SOL":
            base_price = 95.0

        prices = []
        current = base_price

        # generate 20 data points to fit screen
        for _ in range(20):
            # fluctuates 2 percent up or down
            change = random.uniform(-0.02, 0.02)
            current = current * (1 + change)
            prices.append(current)

        return prices

    def get_heatmap_data(self):
        """
        returns top 9 assets for a 3x3 grid display
        """
        # start with existing assets
        data = self.assets[:]

        # if we have less than 9 items fill with dummies for grid look
        while len(data) < 9:
            data.append({
                "symbol": "MOCK",
                "price": 1.0,
                "change": 0.0
            })

        # return exactly 9 items
        return data[:9]