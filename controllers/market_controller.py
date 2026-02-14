# controllers/market_controller.py

import time
from ui.menu_v2 import MenuV2, C

class MarketController:
    def __init__(self, market_service):
        self.market_service = market_service

    def _get_ui_strings(self, lang):
        # helper to get common ui strings based on language
        if lang == "tr":
            return {
                "return_msg": "Geri dönmek için Enter...",
                "input_prefix": "    > ",
                "load_msg": "Veriler yükleniyor...",
                "select_asset": "Varlık Numarası Seçin (0-12): ",
                "invalid": "Geçersiz giriş!",
                "scan": "Blokzincir verileri taranıyor...",
                "not_found": "Varlık bulunamadı!"
            }
        else:
            return {
                "return_msg": "Enter to return...",
                "input_prefix": "    > ",
                "load_msg": "Loading chart data...",
                "select_asset": "Select Asset Number (0-12): ",
                "invalid": "Invalid input!",
                "scan": "Scanning blockchain data...",
                "not_found": "Asset not found!"
            }

    def _format_large_number(self, num):
        # formats large integers into readable strings like 1b or 1m
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        return str(num)

    def view_prices(self, current_lang, user_label, base_path):
        # displays live crypto price table
        title = "KRİPTO FİYATLARI" if current_lang == "tr" else "CRYPTO PRICES"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_top_coins()

        if current_lang == "tr":
            headers = ["#", "VARLIK", "FİYAT", "24S %", "P. DEĞERİ", "HACİM (24S)"]
        else:
            headers = ["#", "ASSET", "PRICE", "24H %", "M. CAP", "VOL (24H)"]

        widths = [4, 16, 14, 12, 12, 12]
        table_rows = []

        for coin in data:
            change_val = coin['change']
            arrow = "▲" if change_val >= 0 else "▼"
            change_str = f"{arrow} {change_val}%"
            asset_str = f"{coin['symbol']} • {coin['name']}"

            row = [
                str(coin["rank"]),
                asset_str,
                f"${coin['price']:,.2f}",
                change_str,
                self._format_large_number(coin["mcap"]),
                self._format_large_number(coin["vol"])
            ]
            table_rows.append(row)

        MenuV2.draw_table(headers, table_rows, widths)
        input(f"\n{ui['return_msg']}")

    def view_listings(self, current_lang, user_label, base_path):
        # displays new asset listings
        title = "YENİ LİSTELEMELER" if current_lang == "tr" else "NEW LISTINGS"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_new_listings()

        if current_lang == "tr":
            headers = ["Sembol", "İsim", "Fiyat", "Perf", "Tarih"]
        else:
            headers = ["Symbol", "Name", "Price", "Perf", "Date"]

        widths = [10, 15, 15, 15, 15]
        table_rows = []

        for coin in data:
            row = [coin["symbol"], coin["name"], f"${coin['price']}", f"{coin['change']}%", coin["date"]]
            table_rows.append(row)

        MenuV2.draw_table(headers, table_rows, widths)
        input(f"\n{ui['return_msg']}")

    def view_gainers(self, current_lang, user_label, base_path):
        # displays top gainers and losers
        title = "KAZANANLAR & KAYBEDENLER" if current_lang == "tr" else "GAINERS & LOSERS"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        gainers, losers = self.market_service.get_gainers_losers()

        t_gainers = "EN ÇOK KAZANANLAR" if current_lang == "tr" else "ROCKET GAINERS"
        t_losers = "EN ÇOK KAYBEDENLER" if current_lang == "tr" else "TOP LOSERS"

        print(f"   {C.GREEN}🚀 {t_gainers}{C.END}")
        for g in gainers:
            print(f"   • {g['symbol']:<10} {C.GREEN}+{g['change']}%{C.END} (${g['price']})")

        print(f"\n   {C.FAIL}📉 {t_losers}{C.END}")
        for l in losers:
            print(f"   • {l['symbol']:<10} {C.FAIL}{l['change']}%{C.END} (${l['price']})")

        input(f"\n\n{ui['return_msg']}")

    def view_sectors(self, current_lang, user_label, base_path):
        # displays performance by market sectors
        title = "SEKTÖR PERFORMANSI" if current_lang == "tr" else "SECTOR PERFORMANCE"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        sectors = self.market_service.get_sector_data(current_lang)

        if current_lang == "tr":
            headers = ["#", "SEKTÖR", "PERF (24S)", "P. DEĞERİ", "LİDER COIN"]
        else:
            headers = ["#", "SECTOR", "PERF (24H)", "M. CAP", "TOP TOKEN"]

        widths = [4, 22, 12, 12, 12]
        table_rows = []

        for s in sectors:
            arrow = "▲" if s['perf'] >= 0 else "▼"
            perf_str = f"{arrow} {s['perf']}%"
            row = [str(s['rank']), s['name'], perf_str, s['mcap'], s['top']]
            table_rows.append(row)

        MenuV2.draw_table(headers, table_rows, widths)
        input(f"\n{ui['return_msg']}")

    def view_fear_greed(self, current_lang, user_label, base_path):
        # shows fear and greed index gauge and history
        t_title = "KORKU & AÇGÖZLÜLÜK ENDEKSİ" if current_lang == "tr" else "FEAR & GREED INDEX"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        fng_data = self.market_service.get_fear_greed_data(current_lang)
        MenuV2.draw_gauge(fng_data["current_value"], fng_data["current_status"])

        if current_lang == "tr":
            h_val = f"{C.CYAN}DEĞER{C.END}"
            headers = ["DÖNEM", h_val, "DURUM"]
        else:
            h_val = f"{C.CYAN}VALUE{C.END}"
            headers = ["PERIOD", h_val, "STATUS"]

        widths = [15, 20, 25]
        table_rows = []

        for item in fng_data["history"]:
            val = item['value']
            if val < 45:
                val_str = f"{C.FAIL}{val}{C.END}"
            elif val > 55:
                val_str = f"{C.GREEN}{val}{C.END}"
            else:
                val_str = f"{C.CYAN}{val}{C.END}"

            table_rows.append([item['period'], val_str, item['status']])

        MenuV2.draw_table(headers, table_rows, widths)
        input(f"\n{ui['return_msg']}")

    def show_chart(self, current_lang, user_label, base_path):
        # allows user to select an asset and view its price chart
        t_title = "TRADINGVIEW GRAFİK" if current_lang == "tr" else "TRADINGVIEW CHART"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        assets = self.market_service.get_all_assets()
        MenuV2.draw_asset_selector(assets, current_lang)

        print(f"{ui['input_prefix']}{ui['select_asset']}", end="")
        choice = input().strip()

        if not choice.isdigit():
            print(f"\n   {C.FAIL}{ui['invalid']}{C.END}")
            time.sleep(1)
            return

        choice_idx = int(choice)
        if choice_idx == 0: return

        if 1 <= choice_idx <= len(assets):
            selected_asset = assets[choice_idx - 1]
            target_symbol = selected_asset['symbol']

            print(f"\n   {C.WARNING}{ui['load_msg']}{C.END}")
            time.sleep(0.5)

            chart_data = self.market_service.get_chart_data(target_symbol)
            MenuV2.draw_simple_chart(target_symbol, chart_data)
            input(f"{ui['return_msg']}")
        else:
            print(f"\n   {C.FAIL}{ui['not_found']}{C.END}")
            time.sleep(1)

    def show_heatmap(self, current_lang, user_label, base_path):
        # displays a visual grid of market performance
        t_title = "PİYASA ISI HARİTASI" if current_lang == "tr" else "MARKET HEATMAP"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        heat_data = self.market_service.get_heatmap_data()
        MenuV2.draw_heatmap(heat_data, current_lang)
        input(f"\n{ui['return_msg']}")

    def show_on_chain(self, current_lang, user_label, base_path):
        # displays blockchain specific data for a chosen asset
        t_title = "ZİNCİR ÜSTÜ ANALİZ" if current_lang == "tr" else "ON-CHAIN ANALYSIS"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        assets = self.market_service.get_all_assets()
        MenuV2.draw_asset_selector(assets, current_lang)

        print(f"{ui['input_prefix']}{ui['select_asset']}", end="")
        choice = input().strip()

        if  choice.isdigit() and int(choice) > 0 and int(choice) <= len(assets):
            selected_asset = assets[int(choice) - 1]
            target_symbol = selected_asset['symbol']

            print(f"\n   {C.WARNING}{ui['scan']}{C.END}")
            time.sleep(1)

            onchain_data = self.market_service.get_onchain_data(target_symbol, current_lang)
            MenuV2.draw_onchain_report(onchain_data)
            input(f"{ui['return_msg']}")
        else:
            if choice != "0":
                print(f"\n   {C.FAIL}{ui['invalid']}{C.END}")
                time.sleep(0.5)

    def show_whale_alerts(self, current_lang, user_label, base_path):
        # displays large transaction alerts
        t_title = "BALİNA ALARMLARI" if current_lang == "tr" else "WHALE ALERTS"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_whale_alerts(current_lang)

        if current_lang == "tr":
            headers = ["COIN", "MİKTAR", "DEĞER (USD)", "KAYNAK -> HEDEF", "ZAMAN"]
        else:
            headers = ["ASSET", "AMOUNT", "VALUE (USD)", "FROM -> TO", "TIME"]

        widths = [8, 15, 18, 35, 12]
        table_rows = []

        for item in data:
            val_str = f"${self._format_large_number(item['value'])}"
            exchanges = ["Binance", "Coinbase", "Kraken", "OKX"]

            if item["to"] in exchanges:
                icon = "🚨"
                flow = f"{item['from']} -> {C.FAIL}{item['to']}{C.END}"
            elif item["from"] in exchanges:
                icon = "🐋"
                flow = f"{C.WARNING}{item['from']}{C.END} -> {item['to']}"
            else:
                icon = "⇄"
                flow = f"{item['from']} -> {item['to']}"

            asset_display = f"{icon} {item['symbol']}"

            row = [
                asset_display,
                f"{item['amount']:,}",
                val_str,
                flow,
                item['time']
            ]
            table_rows.append(row)

        MenuV2.draw_table(headers, table_rows, widths)
        input(f"\n{ui['return_msg']}")

    def show_gas_tracker(self, current_lang, user_label, base_path):
        # shows transaction fee data for various networks
        title = "GAZ ÜCRETİ TAKİPÇİSİ" if current_lang == "tr" else "GAS FEE TRACKER"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_gas_data(current_lang)

        if current_lang == "tr":
            headers = ["AĞ", "GWEI", "TRANSFER ($)", "SWAP ($)", "DURUM"]
        else:
            headers = ["NETWORK", "GWEI", "TRANSFER ($)", "SWAP ($)", "STATUS"]

        widths = [12, 10, 15, 15, 15]
        table_rows = []

        for item in data:
            if item["status_code"] == "LOW":
                color = C.GREEN
                icon = "🟢"
            elif item["status_code"] == "HIGH":
                color = C.FAIL
                icon = "🔴"
            else:
                color = C.WARNING
                icon = "🟡"

            status_display = f"{color}{icon} {item['status']}{C.END}"

            row = [
                item["network"],
                str(item["gwei"]),
                f"${item['transfer']}",
                f"${item['swap']}",
                status_display
            ]
            table_rows.append(row)

        MenuV2.draw_table(headers, table_rows, widths)

        if current_lang == "tr":
            print(f"   {C.GREY}ℹ️  L2 ağları (Arbitrum, OP) genellikle Ethereum'dan 10x daha ucuzdur.{C.END}")
        else:
            print(f"   {C.GREY}ℹ️  L2 networks (Arbitrum, OP) are usually 10x cheaper than Ethereum.{C.END}")

        input(f"\n{ui['return_msg']}")

    def view_economic_calendar(self, current_lang, user_label, base_path):
        # displays upcoming global economic events
        title = "EKONOMİK TAKVİM" if current_lang == "tr" else "ECONOMIC CALENDAR"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_economic_calendar(current_lang)

        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'SAAT':<8}{'DÖVİZ':<6}{'OLAY':<32}{'ETKİ':<18}{'ÖNCEKİ/BEKLENTİ':<20}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'TIME':<8}{'CURR':<6}{'EVENT':<32}{'IMPACT':<18}{'PREV / FORECAST':<20}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 84}{C.END}")

        for item in data:
            time_str = f"{item['time']:<8}"
            curr_str = f"{item['currency']:<6}"

            raw_event = item['event']
            if len(raw_event) > 30:
                raw_event = raw_event[:28] + ".."
            event_str = f"{C.BOLD}{raw_event}{C.END}"
            pad_event = " " * (32 - len(raw_event))

            if item["impact"] == "high":
                vis_impact = f"🔥 {item['impact_label']}"
                colored_impact = f"{C.FAIL}{vis_impact}{C.END}"
            elif item["impact"] == "med":
                vis_impact = f"🔸 {item['impact_label']}"
                colored_impact = f"{C.WARNING}{vis_impact}{C.END}"
            else:
                vis_impact = f"🔹 {item['impact_label']}"
                colored_impact = f"{C.GREY}{vis_impact}{C.END}"

            pad_len = 18 - len(vis_impact) - 1
            if pad_len < 0: pad_len = 0
            impact_str = colored_impact + (" " * pad_len)

            vis_stats = f"{item['prev']} / {item['forecast']}"
            colored_stats = f"{item['prev']} / {C.CYAN}{item['forecast']}{C.END}"
            pad_stats = " " * (20 - len(vis_stats))

            row = f"   {time_str}{curr_str}{event_str}{pad_event}{impact_str}{colored_stats}{pad_stats}"
            print(row)

        print("   " + f"{C.GREY}{'-' * 84}{C.END}")

        if current_lang == "tr":
            print(f"   {C.GREY}ℹ️  Yüksek etkili olaylar (🔥) piyasada sert hareketlere neden olabilir.{C.END}")
        else:
            print(f"   {C.GREY}ℹ️  High impact events (🔥) often cause high volatility in crypto.{C.END}")

        input(f"\n{ui['return_msg']}")