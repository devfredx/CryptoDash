# service/market_service.py

class MarketService:
    def __init__(self):
        # mock database with extended market data
        # rank: siralama, vol: hacim, mcap: piyasa degeri
        self.assets = [
            {"rank": 1, "symbol": "BTC", "name": "Bitcoin", "price": 43250.0, "change": 2.4, "vol": 35000000000, "mcap": 845000000000},
            {"rank": 2, "symbol": "ETH", "name": "Ethereum", "price": 2340.5, "change": -1.2, "vol": 15000000000, "mcap": 278000000000},
            {"rank": 3, "symbol": "SOL", "name": "Solana", "price": 98.4, "change": 5.8, "vol": 4200000000, "mcap": 41000000000},
            {"rank": 4, "symbol": "BNB", "name": "Binance", "price": 315.0, "change": 0.5, "vol": 900000000, "mcap": 48000000000},
            {"rank": 5, "symbol": "XRP", "name": "Ripple", "price": 0.55, "change": -0.8, "vol": 1200000000, "mcap": 29000000000},
            {"rank": 6, "symbol": "ADA", "name": "Cardano", "price": 0.52, "change": -2.1, "vol": 450000000, "mcap": 18000000000},
            {"rank": 7, "symbol": "AVAX", "name": "Avalanche", "price": 36.8, "change": 8.4, "vol": 600000000, "mcap": 13500000000},
        ]

    def get_top_coins(self):
        # return rich asset list
        return self.assets

    def get_new_listings(self):
        # mock list for new tokens
        return [
            {"symbol": "PYTH", "name": "Pyth Network", "price": 0.45, "change": 150.0, "date": "2 Days Ago"},
            {"symbol": "TIA", "name": "Celestia", "price": 12.3, "change": 45.0, "date": "1 Week Ago"},
            {"symbol": "JUP", "name": "Jupiter", "price": 0.65, "change": -5.0, "date": "Just Now"},
        ]

    def get_gainers_losers(self):
        # sort assets by change percentage
        sorted_assets = sorted(self.assets, key=lambda x: x['change'], reverse=True)
        # return top 3 gainers and top 3 losers
        gainers = sorted_assets[:3]
        losers = sorted_assets[-3:]
        return gainers, losers

    def get_all_assets(self):
        # legacy support
        return self.assets