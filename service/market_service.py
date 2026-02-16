# service/market_service.py

class MarketService:
    def __init__(self):
        # Fixed asset list
        self.assets = [
            {"rank": 1, "symbol": "BTC  ", "name": "Bitcoin", "price": 52150.0, "change": 2.4, "vol": 35000000000,
             "mcap": 980000000000},
            {"rank": 2, "symbol": "ETH  ", "name": "Ethereum", "price": 2980.5, "change": 1.2, "vol": 15000000000,
             "mcap": 350000000000},
            {"rank": 3, "symbol": "BNB  ", "name": "Binance", "price": 385.0, "change": -0.5, "vol": 900000000,
             "mcap": 58000000000},
            {"rank": 4, "symbol": "SOL  ", "name": "Solana", "price": 112.4, "change": 5.8, "vol": 4200000000,
             "mcap": 49000000000},
            {"rank": 5, "symbol": "XRP  ", "name": "Ripple", "price": 0.58, "change": -0.8, "vol": 1200000000,
             "mcap": 31000000000},
            {"rank": 6, "symbol": "ADA  ", "name": "Cardano", "price": 0.62, "change": -2.1, "vol": 450000000,
             "mcap": 21000000000},
            {"rank": 7, "symbol": "AVAX ", "name": "Avalanche", "price": 41.8, "change": 8.4, "vol": 600000000,
             "mcap": 15500000000},
            {"rank": 8, "symbol": "DOGE ", "name": "Dogecoin", "price": 0.088, "change": 12.5, "vol": 800000000,
             "mcap": 12000000000},
            {"rank": 9, "symbol": "TRX  ", "name": "Tron", "price": 0.13, "change": 0.4, "vol": 300000000,
             "mcap": 11000000000},
            {"rank": 10, "symbol": "LINK ", "name": "Chainlink", "price": 19.5, "change": 3.2, "vol": 500000000,
             "mcap": 10500000000},
            {"rank": 11, "symbol": "DOT  ", "name": "Polkadot", "price": 7.8, "change": -1.5, "vol": 250000000,
             "mcap": 9800000000},
            {"rank": 12, "symbol": "MATIC", "name": "Polygon", "price": 0.98, "change": 1.1, "vol": 320000000,
             "mcap": 9200000000},
        ]

    def get_top_coins(self):
        return self.assets

    def get_new_listings(self, lang="en"):
        # return mock new asset listings with localized dates
        if lang == "tr":
            return [
                {"symbol": "PIXEL", "name": "Pixels", "price": 0.52, "change": 1250.0, "date": "1 Gün Önce"},
                {"symbol": "STRK", "name": "Starknet", "price": 2.10, "change": 0.0, "date": "Yakında"},
                {"symbol": "DYM", "name": "Dymension", "price": 7.45, "change": 45.0, "date": "1 Hafta Önce"},
            ]
        return [
            {"symbol": "PIXEL", "name": "Pixels", "price": 0.52, "change": 1250.0, "date": "1 Day Ago"},
            {"symbol": "STRK", "name": "Starknet", "price": 2.10, "change": 0.0, "date": "Coming Soon"},
            {"symbol": "DYM", "name": "Dymension", "price": 7.45, "change": 45.0, "date": "1 Week Ago"},
        ]

    def get_gainers_losers(self):
        # Fixed sorting based on change
        sorted_assets = sorted(self.assets, key=lambda x: x['change'], reverse=True)
        gainers = sorted_assets[:3]
        losers = sorted_assets[-3:]
        return gainers, losers

    def get_sector_data(self, lang="en"):
        if lang == "tr":
            return [
                {"rank": 1, "name": "Katman 1 (L1)", "perf": 1.2, "mcap": "1.6T", "top": "BTC"},
                {"rank": 2, "name": "Akıllı Sözleşmeler", "perf": -0.5, "mcap": "550B", "top": "ETH"},
                {"rank": 3, "name": "Yapay Zeka (AI)", "perf": 16.5, "mcap": "18B", "top": "FET"},
                {"rank": 4, "name": "DeFi (Finans)", "perf": 2.1, "mcap": "75B", "top": "UNI"},
                {"rank": 5, "name": "Oyun / Metaverse", "perf": -3.2, "mcap": "22B", "top": "IMX"},
                {"rank": 6, "name": "Meme Coinler", "perf": 12.4, "mcap": "35B", "top": "DOGE"},
                {"rank": 7, "name": "Gerçek Varlıklar (RWA)", "perf": 0.8, "mcap": "6B", "top": "ONDO"},
            ]
        else:
            return [
                {"rank": 1, "name": "Layer 1", "perf": 1.2, "mcap": "1.6T", "top": "BTC"},
                {"rank": 2, "name": "Smart Contracts", "perf": -0.5, "mcap": "550B", "top": "ETH"},
                {"rank": 3, "name": "AI & Big Data", "perf": 16.5, "mcap": "18B", "top": "FET"},
                {"rank": 4, "name": "DeFi (Finance)", "perf": 2.1, "mcap": "75B", "top": "UNI"},
                {"rank": 5, "name": "Gaming / Metaverse", "perf": -3.2, "mcap": "22B", "top": "IMX"},
                {"rank": 6, "name": "Meme Coins", "perf": 12.4, "mcap": "35B", "top": "DOGE"},
                {"rank": 7, "name": "RWA (Real World)", "perf": 0.8, "mcap": "6B", "top": "ONDO"},
            ]

    def get_all_assets(self):
        return self.assets

    def get_fear_greed_data(self, lang="en"):
        # Fixed data for simulation
        current_score = 74
        labels = {
            "en": {"greed": "Greed", "neutral": "Neutral", "extreme_fear": "Extreme Fear",
                   "periods": ["Now", "Yesterday", "Last Week", "Last Month"]},
            "tr": {"greed": "Açgözlülük", "neutral": "Nötr", "extreme_fear": "Aşırı Korku",
                   "periods": ["Şimdi", "Dün", "Geçen Hafta", "Geçen Ay"]}
        }
        txt = labels.get(lang, labels["en"])

        history = [
            {"period": txt["periods"][0], "value": current_score, "status": txt["greed"]},
            {"period": txt["periods"][1], "value": 65, "status": txt["greed"]},
            {"period": txt["periods"][2], "value": 45, "status": txt["neutral"]},
            {"period": txt["periods"][3], "value": 20, "status": txt["extreme_fear"]},
        ]
        return {
            "current_value": current_score,
            "current_status": txt["greed"],
            "history": history
        }

    def get_chart_data(self, symbol):
        """
        Returns fixed pattern chart data for stability
        """
        base_price = 100.0
        for asset in self.assets:
            if asset['symbol'] == symbol:
                base_price = asset['price']
                break

        # Fixed pattern calculation
        multipliers = [1.0, 1.01, 1.02, 1.015, 1.03, 1.025, 1.04, 1.035, 1.05, 1.045,
                       1.06, 1.055, 1.07, 1.06, 1.05, 1.04, 1.03, 1.035, 1.04, 1.05]

        prices = [base_price * m for m in multipliers]
        return prices

    def get_heatmap_data(self):
        data = self.assets[:]
        return data[:9]

    def get_onchain_data(self, symbol, lang="en"):
        # Completely fixed onchain data
        if symbol == "BTC":
            inflow, outflow, active, conc, net = 12500, 18400, 950000, 12.5, 5900
        elif symbol == "ETH":
            inflow, outflow, active, conc, net = 45000, 42000, 420000, 35.2, -3000
        else:
            inflow, outflow, active, conc, net = 5000, 4500, 25000, 45.0, -500

        if lang == "tr":
            signal = "YÜKSELİŞ (BULLISH)" if net > 0 else "DÜŞÜŞ (BEARISH)"
            labels = {"in": "Borsaya Giren", "out": "Borsadan Çıkan", "net": "Net Akış", "addr": "Aktif Adres",
                      "whale": "Balina Konsantrasyonu"}
        else:
            signal = "BULLISH" if net > 0 else "BEARISH"
            labels = {"in": "Exchange Inflow", "out": "Exchange Outflow", "net": "Net Flow", "addr": "Active Addresses",
                      "whale": "Whale Concentration"}

        return {
            "symbol": symbol,
            "inflow": inflow,
            "outflow": outflow,
            "net_flow": net,
            "signal": signal,
            "active_addresses": active,
            "whale_conc": conc,
            "labels": labels
        }

    def get_whale_alerts(self, lang="en"):
        """
        Returns a fixed list of alerts without random generation
        """
        if lang == "tr":
            suffix = "dk önce"
            w_unknown = "Bilinmeyen"
            w_cold = "Soğuk Cüzdan"
        else:
            suffix = "m ago"
            w_unknown = "Unknown Wallet"
            w_cold = "Cold Storage"

        # Fixed list appears the same every time
        return [
            {"symbol": "BTC", "amount": 150, "value": 7822500, "from": w_unknown, "to": "Binance",
             "time": f"5{suffix}"},
            {"symbol": "ETH", "amount": 2500, "value": 7451250, "from": "Kraken", "to": w_unknown,
             "time": f"12{suffix}"},
            {"symbol": "SOL", "amount": 150000, "value": 16860000, "from": w_cold, "to": "Coinbase",
             "time": f"18{suffix}"},
            {"symbol": "XRP", "amount": 5000000, "value": 2900000, "from": "Binance", "to": "OKX",
             "time": f"24{suffix}"},
            {"symbol": "DOGE    ", "amount": 10000000, "value": 880000, "from": w_unknown, "to": w_unknown,
             "time": f"32{suffix}"},
            {"symbol": "MATIC   ", "amount": 2000000, "value": 1960000, "from": "Polygon Bridge", "to": w_unknown,
             "time": f"40{suffix}"},
            {"symbol": "BTC", "amount": 55, "value": 2868250, "from": "Coinbase", "to": w_cold, "time": f"45{suffix}"},
            {"symbol": "BNB", "amount": 5000, "value": 1925000, "from": w_unknown, "to": "Binance",
             "time": f"58{suffix}"},
        ]

    def get_gas_data(self, lang="en"):
        """
        Returns fixed gas fee data without random volatility
        """
        if lang == "tr":
            s_low, s_avg, s_high = "DÜŞÜK", "ORTA", "YÜKSEK"
            code_low, code_avg, code_high = "LOW", "AVG", "HIGH"
        else:
            s_low, s_avg, s_high = "LOW", "AVERAGE", "HIGH"
            code_low, code_avg, code_high = "LOW", "AVG", "HIGH"

        # Manually entered fixed data
        return [
            {"network": "Ethereum", "gwei": 45, "transfer": 6.50, "swap": 35.20, "status": s_high,
             "status_code": code_high},
            {"network": "Bitcoin (BTC)", "gwei": 28, "transfer": 12.50, "swap": 0.00, "status": s_avg,
             "status_code": code_avg},
            {"network": "Arbitrum", "gwei": 0.1, "transfer": 0.01, "swap": 0.03, "status": s_low,
             "status_code": code_low},
            {"network": "Optimism", "gwei": 0.1, "transfer": 0.01, "swap": 0.03, "status": s_low,
             "status_code": code_low},
            {"network": "Base", "gwei": 0.05, "transfer": 0.01, "swap": 0.02, "status": s_low, "status_code": code_low},
            {"network": "zkSync Era", "gwei": 0.2, "transfer": 0.02, "swap": 0.05, "status": s_low,
             "status_code": code_low},
            {"network": "Polygon", "gwei": 35, "transfer": 0.02, "swap": 0.08, "status": s_avg,
             "status_code": code_avg},
            {"network": "BSC (Binance)", "gwei": 3, "transfer": 0.03, "swap": 0.15, "status": s_low,
             "status_code": code_low},
            {"network": "Avalanche", "gwei": 28, "transfer": 0.08, "swap": 0.45, "status": s_avg,
             "status_code": code_avg},
            {"network": "Solana", "gwei": 15, "transfer": 0.00, "swap": 0.00, "status": s_low, "status_code": code_low},
        ]

    def get_economic_calendar(self, lang="en"):
        """
        Generates mock economic calendar events
        """
        # Localized texts
        if lang == "tr":
            impact_labels = {"high": "YÜKSEK", "med": "ORTA", "low": "DÜŞÜK"}
            events = [
                {"time": "15:30", "currency": "USD", "event": "Tüketici Fiyat Endeksi (TÜFE) - Yıllık",
                 "impact": "high", "prev": "3.4%", "forecast": "3.2%"},
                {"time": "15:30", "currency": "USD", "event": "Tarım Dışı İstihdam (NFP)", "impact": "high",
                 "prev": "216K", "forecast": "180K"},
                {"time": "21:00", "currency": "USD", "event": "Fed Faiz Kararı", "impact": "high", "prev": "5.50%",
                 "forecast": "5.50%"},
                {"time": "21:30", "currency": "USD", "event": "FOMC Basın Toplantısı", "impact": "high", "prev": "-",
                 "forecast": "-"},
                {"time": "12:00", "currency": "EUR", "event": "Euro Bölgesi TÜFE (Yıllık)", "impact": "med",
                 "prev": "2.9%", "forecast": "2.8%"},
                {"time": "16:45", "currency": "USD", "event": "Hizmet PMI Verisi", "impact": "med", "prev": "51.4",
                 "forecast": "52.0%"},
                {"time": "17:30", "currency": "USD", "event": "Ham Petrol Stokları", "impact": "low", "prev": "-2.5M",
                 "forecast": "-1.0M"},
                {"time": "09:00", "currency": "GBP", "event": "GSYİH (GDP) Büyüme Oranı", "impact": "med",
                 "prev": "0.1%", "forecast": "0.0%"},
            ]
        else:
            impact_labels = {"high": "HIGH", "med": "MEDIUM", "low": "LOW"}
            events = [
                {"time": "15:30", "currency": "USD", "event": "Core CPI (YoY)", "impact": "high", "prev": "3.4%",
                 "forecast": "3.2%"},
                {"time": "15:30", "currency": "USD", "event": "Non-Farm Payrolls", "impact": "high", "prev": "216K",
                 "forecast": "180K"},
                {"time": "21:00", "currency": "USD", "event": "Fed Interest Rate Decision", "impact": "high",
                 "prev": "5.50%", "forecast": "5.50%"},
                {"time": "21:30", "currency": "USD", "event": "FOMC Press Conference", "impact": "high", "prev": "-",
                 "forecast": "-"},
                {"time": "12:00", "currency": "EUR", "event": "Eurozone CPI (YoY)", "impact": "med", "prev": "2.9%",
                 "forecast": "2.8%"},
                {"time": "16:45", "currency": "USD", "event": "Services PMI", "impact": "med", "prev": "51.4",
                 "forecast": "52.0%"},
                {"time": "17:30", "currency": "USD", "event": "Crude Oil Inventories", "impact": "low", "prev": "-2.5M",
                 "forecast": "-1.0M"},
                {"time": "09:00", "currency": "GBP", "event": "GDP Growth Rate", "impact": "med", "prev": "0.1%",
                 "forecast": "0.0%"},
            ]

        # Add localized impact label to data
        processed_data = []
        for item in events:
            item["impact_label"] = impact_labels[item["impact"]]
            processed_data.append(item)

        return processed_data

    def get_ico_list(self, lang="en"):
        # return a full list of 12 projects to match menu prompt
        if lang == "tr":
            return [
                {"id": 1, "name": "Monad", "type": "ICO", "cat": "Layer 1", "status": "Yakında", "goal": "$200M"},
                {"id": 2, "name": "Berachain", "type": "Airdrop", "cat": "DeFi", "status": "Testnet", "goal": "Belirsiz"},
                {"id": 3, "name": "Scroll", "type": "ICO", "cat": "Layer 2", "status": "Aktif", "goal": "$50M"},
                {"id": 4, "name": "Fuel Network", "type": "Airdrop", "cat": "Modular", "status": "Yakında", "goal": "Belirsiz"},
                {"id": 5, "name": "Celestia", "type": "Airdrop", "cat": "Data Avail.", "status": "Aktif", "goal": "$56M"},
                {"id": 6, "name": "EigenLayer", "type": "Airdrop", "cat": "Restaking", "status": "Testnet", "goal": "Belirsiz"},
                {"id": 7, "name": "LayerZero", "type": "Airdrop", "cat": "Interop.", "status": "Yakında", "goal": "Belirsiz"},
                {"id": 8, "name": "Starknet", "type": "Airdrop", "cat": "ZK-Rollup", "status": "Aktif", "goal": "$280M"},
                {"id": 9, "name": "Taiko", "type": "ICO", "cat": "ZK-EVM", "status": "Testnet", "goal": "$22M"},
                {"id": 10, "name": "Linea", "type": "Airdrop", "cat": "ZK-EVM", "status": "Testnet", "goal": "Belirsiz"},
                {"id": 11, "name": "Aleo", "type": "ICO", "cat": "Privacy L1", "status": "Yakında", "goal": "$200M"},
                {"id": 12, "name": "Zora", "type": "Airdrop", "cat": "NFT L2", "status": "Aktif", "goal": "Belirsiz"}
            ]
        return [
            {"id": 1, "name": "Monad", "type": "ICO", "cat": "Layer 1", "status": "Upcoming", "goal": "$200M"},
            {"id": 2, "name": "Berachain", "type": "Airdrop", "cat": "DeFi", "status": "Testnet", "goal": "TBA"},
            {"id": 3, "name": "Scroll", "type": "ICO", "cat": "Layer 2", "status": "Active", "goal": "$50M"},
            {"id": 4, "name": "Fuel Network", "type": "Airdrop", "cat": "Modular", "status": "Upcoming", "goal": "TBA"},
            {"id": 5, "name": "Celestia", "type": "Airdrop", "cat": "Data Avail.", "status": "Active", "goal": "$56M"},
            {"id": 6, "name": "EigenLayer", "type": "Airdrop", "cat": "Restaking", "status": "Testnet", "goal": "TBA"},
            {"id": 7, "name": "LayerZero", "type": "Airdrop", "cat": "Interop.", "status": "Upcoming", "goal": "TBA"},
            {"id": 8, "name": "Starknet", "type": "Airdrop", "cat": "ZK-Rollup", "status": "Active", "goal": "$280M"},
            {"id": 9, "name": "Taiko", "type": "ICO", "cat": "ZK-EVM", "status": "Testnet", "goal": "$22M"},
            {"id": 10, "name": "Linea", "type": "Airdrop", "cat": "ZK-EVM", "status": "Testnet", "goal": "TBA"},
            {"id": 11, "name": "Aleo", "type": "ICO", "cat": "Privacy L1", "status": "Upcoming", "goal": "$200M"},
            {"id": 12, "name": "Zora", "type": "Airdrop", "cat": "NFT L2", "status": "Active", "goal": "TBA"}
        ]

    def get_ico_details(self, project_id, lang="en"):
        # return comprehensive mock data for 12 projects with variety
        details = {
            1: {  # Monad
                "en": {"desc": "Ultra high performance EVM compatible Layer 1", "platform": "Monad Labs",
                       "lock": "24 Months", "investors": "Dragonfly, Paradigm", "utility": "Gas, Governance",
                       "risk": "Low"},
                "tr": {"desc": "Ultra yüksek performanslı EVM uyumlu Katman 1", "platform": "Monad Labs",
                       "lock": "24 Ay", "investors": "Dragonfly, Paradigm", "utility": "Gas, Yönetişim",
                       "risk": "Düşük"}
            },
            2: {  # Berachain
                "en": {"desc": "DeFi focused L1 built on Cosmos SDK", "platform": "Bera Ecosystem", "lock": "No Lock",
                       "investors": "Polychain, OKX", "utility": "Staking, Gas", "risk": "Medium"},
                "tr": {"desc": "Cosmos SDK üzerine inşa edilmiş DeFi odaklı L1", "platform": "Bera Ekosistemi",
                       "lock": "Kilit Yok", "investors": "Polychain, OKX", "utility": "Staking, Gas", "risk": "Orta"}
            },
            3: {  # Scroll
                "en": {"desc": "Native zkEVM scaling solution for Ethereum", "platform": "Scroll Foundation",
                       "lock": "18 Months", "investors": "Polychain, Sequoia", "utility": "Network Fees",
                       "risk": "Low"},
                "tr": {"desc": "Ethereum için yerel zkEVM ölçeklendirme çözümü", "platform": "Scroll Vakfı",
                       "lock": "18 Ay", "investors": "Polychain, Sequoia", "utility": "Ağ Ücretleri", "risk": "Düşük"}
            },
            8: {  # Starknet
                "en": {"desc": "Validity Rollup L2 using STARK proofs", "platform": "StarkWare", "lock": "Released",
                       "investors": "Vitalik Buterin, Paradigm", "utility": "Gas, Governance", "risk": "Very Low"},
                "tr": {"desc": "STARK kanıtlarını kullanan Validity Rollup L2", "platform": "StarkWare",
                       "lock": "Açıldı", "investors": "Vitalik Buterin, Paradigm", "utility": "Gas, Yönetişim",
                       "risk": "Çok Düşük"}
            }
        }

        # dynamic fallback for other projects
        default_data = {
            "en": {"desc": "Emerging decentralized infrastructure project", "platform": "Independent Launch",
                   "lock": "Vesting Plan", "investors": "Venture Capitals", "utility": "Ecosystem Rewards",
                   "risk": "High"},
            "tr": {"desc": "Gelişmekte olan merkeziyetsiz altyapı projesi", "platform": "Bağımsız Lansman",
                   "lock": "Hakediş Planı", "investors": "Risk Sermayeleri", "utility": "Ekosistem Ödülleri",
                   "risk": "Yüksek"}
        }

        return details.get(project_id, {"en": default_data["en"], "tr": default_data["tr"]})[lang]

    def get_unlock_list(self, lang="en"):
        # return a full list of 12 token unlock events for consistency
        if lang == "tr":
            return [
                {"id": 1, "symbol": "ARB", "name": "Arbitrum", "date": "22 Şub 2026", "amount": "92.6M",
                 "value": "$112M", "ratio": "1.1%"},
                {"id": 2, "symbol": "SOL", "name": "Solana", "date": "01 Mar 2026", "amount": "1.2M", "value": "$145M",
                 "ratio": "0.3%"},
                {"id": 3, "symbol": "OP", "name": "Optimism", "date": "15 Mar 2026", "amount": "31.4M", "value": "$88M",
                 "ratio": "2.8%"},
                {"id": 4, "symbol": "SUI", "name": "Sui", "date": "03 Nis 2026", "amount": "65M", "value": "$95M",
                 "ratio": "4.2%"},
                {"id": 5, "symbol": "DYX", "name": "dYdX", "date": "12 Nis 2026", "amount": "2.1M", "value": "$6.4M",
                 "ratio": "0.8%"},
                {"id": 6, "symbol": "APT", "name": "Aptos", "date": "18 Nis 2026", "amount": "11.3M", "value": "$102M",
                 "ratio": "2.5%"},
                {"id": 7, "symbol": "IMX", "name": "Immutable", "date": "25 Nis 2026", "amount": "25.5M",
                 "value": "$58M", "ratio": "1.9%"},
                {"id": 8, "symbol": "TIA", "name": "Celestia", "date": "30 Nis 2026", "amount": "1.1M", "value": "$12M",
                 "ratio": "0.5%"},
                {"id": 9, "symbol": "STRK", "name": "Starknet", "date": "05 May 2026", "amount": "64M",
                 "value": "$134M", "ratio": "3.1%"},
                {"id": 10, "symbol": "SEI", "name": "Sei Network", "date": "15 May 2026", "amount": "125M",
                 "value": "$82M", "ratio": "5.4%"},
                {"id": 11, "symbol": "W", "name": "Wormhole", "date": "22 May 2026", "amount": "18M", "value": "$11M",
                 "ratio": "1.0%"},
                {"id": 12, "symbol": "ZETA", "name": "ZetaChain", "date": "28 May 2026", "amount": "5.2M",
                 "value": "$8M", "ratio": "2.2%"}
            ]
        return [
            {"id": 1, "symbol": "ARB", "name": "Arbitrum", "date": "Feb 22, 2026", "amount": "92.6M", "value": "$112M",
             "ratio": "1.1%"},
            {"id": 2, "symbol": "SOL", "name": "Solana", "date": "Mar 01, 2026", "amount": "1.2M", "value": "$145M",
             "ratio": "0.3%"},
            {"id": 3, "symbol": "OP", "name": "Optimism", "date": "Mar 15, 2026", "amount": "31.4M", "value": "$88M",
             "ratio": "2.8%"},
            {"id": 4, "symbol": "SUI", "name": "Sui", "date": "Apr 03, 2026", "amount": "65M", "value": "$95M",
             "ratio": "4.2%"},
            {"id": 5, "symbol": "DYX", "name": "dYdX", "date": "Apr 12, 2026", "amount": "2.1M", "value": "$6.4M",
             "ratio": "0.8%"},
            {"id": 6, "symbol": "APT", "name": "Aptos", "date": "Apr 18, 2026", "amount": "11.3M", "value": "$102M",
             "ratio": "2.5%"},
            {"id": 7, "symbol": "IMX", "name": "Immutable", "date": "Apr 25, 2026", "amount": "25.5M", "value": "$58M",
             "ratio": "1.9%"},
            {"id": 8, "symbol": "TIA", "name": "Celestia", "date": "Apr 30, 2026", "amount": "1.1M", "value": "$12M",
             "ratio": "0.5%"},
            {"id": 9, "symbol": "STRK", "name": "Starknet", "date": "May 05, 2026", "amount": "64M", "value": "$134M",
             "ratio": "3.1%"},
            {"id": 10, "symbol": "SEI", "name": "Sei Network", "date": "May 15, 2026", "amount": "125M",
             "value": "$82M", "ratio": "5.4%"},
            {"id": 11, "symbol": "W", "name": "Wormhole", "date": "May 22, 2026", "amount": "18M", "value": "$11M",
             "ratio": "1.0%"},
            {"id": 12, "symbol": "ZETA", "name": "ZetaChain", "date": "May 28, 2026", "amount": "5.2M", "value": "$8M",
             "ratio": "2.2%"}
        ]

    def get_unlock_details(self, project_id, lang="en"):
        # return specific allocation breakdown for all 12 projects
        data = {
            1: {"team": "40%", "investors": "35%", "eco": "25%"},  # ARB
            2: {"team": "10%", "investors": "10%", "eco": "80%"},  # SOL
            3: {"team": "25%", "investors": "25%", "eco": "50%"},  # OP
            4: {"team": "30%", "investors": "40%", "eco": "30%"},  # SUI
            5: {"team": "20%", "investors": "50%", "eco": "30%"},  # DYX
            6: {"team": "35%", "investors": "35%", "eco": "30%"},  # APT
            7: {"team": "25%", "investors": "20%", "eco": "55%"},  # IMX
            8: {"team": "20%", "investors": "30%", "eco": "50%"},  # TIA
            9: {"team": "30%", "investors": "30%", "eco": "40%"},  # STRK
            10: {"team": "20%", "investors": "20%", "eco": "60%"},  # SEI
            11: {"team": "15%", "investors": "15%", "eco": "70%"},  # W
            12: {"team": "25%", "investors": "35%", "eco": "40%"}  # ZETA
        }

        # fallback to neutral distribution if ID not found
        res = data.get(project_id, {"team": "33%", "investors": "33%", "eco": "34%"})

        labels = {
            "en": {"t": "Team/Advisors", "i": "Investors", "e": "Ecosystem/Rewards"},
            "tr": {"t": "Ekip/Danışmanlar", "i": "Yatırımcılar", "e": "Ekosistem/Ödüller"}
        }[lang]

        return {
            "breakdown": [
                {"label": labels["t"], "val": res["team"]},
                {"label": labels["i"], "val": res["investors"]},
                {"label": labels["e"], "val": res["eco"]}
            ]
        }