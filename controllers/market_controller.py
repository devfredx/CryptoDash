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
        # converts large numbers into readable strings with b or m suffix
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        return str(num)

    def view_prices(self, current_lang, user_label, base_path):
        # displays live crypto prices with manual alignment logic
        title = "KRİPTO FİYATLARI" if current_lang == "tr" else "CRYPTO PRICES"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_top_coins()

        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'VARLIK':<18}{'FİYAT':<14}{'24S %':<12}{'P. DEĞERİ':<12}{'HACİM':<12}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'ASSET':<18}{'PRICE':<14}{'24H %':<12}{'M. CAP':<12}{'VOLUME':<12}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 72}{C.END}")

        for coin in data:
            rank = f"{str(coin['rank']):<4}"
            asset_name = f"{coin['symbol']} • {coin['name']}"
            asset_str = f"{asset_name:<18}"
            price_str = f"${coin['price']:,.2f}"
            price_pad = f"{price_str:<14}"

            change_val = coin['change']
            arrow = "▲" if change_val >= 0 else "▼"
            vis_change = f"{arrow} {abs(change_val)}%"
            color = C.GREEN if change_val >= 0 else C.FAIL
            change_str = f"{color}{vis_change}{C.END}" + (" " * (12 - len(vis_change)))

            mcap = f"{self._format_large_number(coin['mcap']):<12}"
            vol = f"{self._format_large_number(coin['vol']):<12}"

            print(f"   {rank}{asset_str}{price_pad}{change_str}{mcap}{vol}")

        input(f"\n{ui['return_msg']}")

    def view_listings(self, current_lang, user_label, base_path):
        # displays new asset listings with localized dates and manual alignment
        title = "YENİ LİSTELEMELER" if current_lang == "tr" else "NEW LISTINGS"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        # request localized listing data from service
        data = self.market_service.get_new_listings(current_lang)

        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'SEMBOL':<10}{'İSİM':<18}{'FİYAT':<12}{'PERF':<12}{'TARİH':<15}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'SYMBOL':<10}{'NAME':<18}{'PRICE':<12}{'PERF':<12}{'DATE':<15}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 67}{C.END}")

        for coin in data:
            sym = f"{coin['symbol']:<10}"
            name = f"{coin['name']:<18}"
            price = f"${coin['price']:<12}"

            # format performance string with color
            perf_val = f"{coin['change']}%"
            perf_str = f"{C.GREEN}{perf_val}{C.END}" + (" " * (12 - len(perf_val)))

            # date is now localized by the service
            date = f"{coin['date']:<15}"

            print(f"   {sym}{name}{price}{perf_str}{date}")

        input(f"\n{ui['return_msg']}")

    def view_gainers(self, current_lang, user_label, base_path):
        # shows top gainers and losers in a simple list format
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
        # views performance by market sectors with fixed padding
        title = "SEKTÖR PERFORMANSI" if current_lang == "tr" else "SECTOR PERFORMANCE"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        sectors = self.market_service.get_sector_data(current_lang)

        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'SEKTÖR':<25}{'PERF (24S)':<15}{'P. DEĞERİ':<12}{'LİDER':<10}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'SECTOR':<25}{'PERF (24H)':<15}{'M. CAP':<12}{'TOP':<10}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 66}{C.END}")

        for s in sectors:
            rank = f"{str(s['rank']):<4}"
            name = f"{s['name']:<25}"
            perf_val = s['perf']
            arrow = "▲" if perf_val >= 0 else "▼"
            vis_perf = f"{arrow} {perf_val}%"
            color = C.GREEN if perf_val >= 0 else C.FAIL
            perf_str = f"{color}{vis_perf}{C.END}" + (" " * (15 - len(vis_perf)))
            mcap = f"{s['mcap']:<12}"
            top = f"{s['top']:<10}"
            print(f"   {rank}{name}{perf_str}{mcap}{top}")

        input(f"\n{ui['return_msg']}")

    def view_fear_greed(self, current_lang, user_label, base_path):
        # shows fear and greed index gauge and history table
        t_title = "KORKU & AÇGÖZLÜLÜK ENDEKSİ" if current_lang == "tr" else "FEAR & GREED INDEX"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        fng_data = self.market_service.get_fear_greed_data(current_lang)

        # define localized sentiment title for the gauge
        t_sentiment = "PİYASA DUYARLILIĞI" if current_lang == "tr" else "MARKET SENTIMENT"
        MenuV2.draw_gauge(fng_data["current_value"], fng_data["current_status"], title=t_sentiment)

        # print history table using manual alignment logic
        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'DÖNEM':<15}{'DEĞER':<20}{'DURUM':<25}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'PERIOD':<15}{'VALUE':<20}{'STATUS':<25}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 60}{C.END}")

        for item in fng_data["history"]:
            period = f"{item['period']:<15}"

            # handle colored value column
            val = item['value']
            if val < 45:
                color = C.FAIL
            elif val > 55:
                color = C.GREEN
            else:
                color = C.CYAN

            val_vis = str(val)
            val_str = f"{color}{val_vis}{C.END}" + (" " * (20 - len(val_vis)))
            status = f"{item['status']:<25}"

            print(f"   {period}{val_str}{status}")

        input(f"\n{ui['return_msg']}")

    def show_chart(self, current_lang, user_label, base_path):
        # prepare screen and show asset list
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

            # clear screen and redraw header for clean chart view
            MenuV2.prepare_content_screen(base_path + [t_title, target_symbol], user_info=user_label)

            # display selection info
            selection_text = "Seçilen Varlık" if current_lang == "tr" else "Selected Asset"
            print(f"   {C.BOLD}{selection_text}: {C.CYAN}{target_symbol} ({selected_asset['name']}){C.END}\n")

            print(f"   {C.WARNING}{ui['load_msg']}{C.END}")
            time.sleep(0.5)

            # render chart with language support
            chart_data = self.market_service.get_chart_data(target_symbol)
            MenuV2.draw_simple_chart(target_symbol, chart_data, current_lang)

            # handle return interaction
            input(f"{ui['return_msg']}")
        else:
            print(f"\n   {C.FAIL}{ui['not_found']}{C.END}")
            time.sleep(1)

    def show_heatmap(self, current_lang, user_label, base_path):
        # displays visual heatmap of the top assets
        t_title = "PİYASA ISI HARİTASI" if current_lang == "tr" else "MARKET HEATMAP"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        heat_data = self.market_service.get_heatmap_data()
        MenuV2.draw_heatmap(heat_data, current_lang)
        input(f"\n{ui['return_msg']}")

    def show_on_chain(self, current_lang, user_label, base_path):
        # prepare screen and display asset list for on chain analysis
        t_title = "ZİNCİR ÜSTÜ ANALİZ" if current_lang == "tr" else "ON-CHAIN ANALYSIS"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        assets = self.market_service.get_all_assets()
        MenuV2.draw_asset_selector(assets, current_lang)

        print(f"{ui['input_prefix']}{ui['select_asset']}", end="")
        choice = input().strip()

        if choice.isdigit() and 1 <= int(choice) <= len(assets):
            selected_asset = assets[int(choice) - 1]
            target_symbol = selected_asset['symbol']

            # clear screen and redraw header with asset symbol for focus
            MenuV2.prepare_content_screen(base_path + [t_title, target_symbol], user_info=user_label)

            # print localized selection details
            selection_text = "Seçilen Varlık" if current_lang == "tr" else "Selected Asset"
            print(f"   {C.BOLD}{selection_text}: {C.CYAN}{target_symbol} ({selected_asset['name']}){C.END}\n")

            print(f"   {C.WARNING}{ui['scan']}{C.END}")
            time.sleep(1)

            # render on chain report with language support
            onchain_data = self.market_service.get_onchain_data(target_symbol, current_lang)
            MenuV2.draw_onchain_report(onchain_data, current_lang)

            # handle return to menu
            input(f"{ui['return_msg']}")
        else:
            if choice != "0":
                print(f"\n   {C.FAIL}{ui['invalid']}{C.END}")
                time.sleep(0.5)

    def show_whale_alerts(self, current_lang, user_label, base_path):
        # display whale alerts with fixed manual alignment
        t_title = "BALİNA ALARMLARI" if current_lang == "tr" else "WHALE ALERTS"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_whale_alerts(current_lang)

        # print table headers with manual spacing
        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'COIN':<10}{'MİKTAR':<15}{'DEĞER (USD)':<15}{'KAYNAK -> HEDEF':<35}{'ZAMAN':<10}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'ASSET':<10}{'AMOUNT':<15}{'VALUE (USD)':<15}{'FROM -> TO':<35}{'TIME':<10}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 85}{C.END}")

        # process each alert with manual padding logic
        for item in data:
            # format asset column with icons
            exchanges = ["Binance", "Coinbase", "Kraken", "OKX"]
            icon = "🚨" if item["to"] in exchanges else ("🐋" if item["from"] in exchanges else "⇄")

            vis_asset = f"{icon} {item['symbol']}"
            colored_asset = f"{C.BOLD}{vis_asset}{C.END}"
            # compensate for emoji width in terminal
            pad_asset = " " * (10 - len(vis_asset) - 1)

            # format transaction amount
            amount_val = f"{item['amount']:,}"
            amount_str = f"{amount_val:<15}"

            # format usd value with cyan color
            val_vis = f"${self._format_large_number(item['value'])}"
            colored_val = f"{C.CYAN}{val_vis}{C.END}"
            pad_val = " " * (15 - len(val_vis))

            # format source and destination with exchange highlights
            flow_vis = f"{item['from']} -> {item['to']}"
            if item["to"] in exchanges:
                # highlight destination red for exchanges
                flow_colored = f"{item['from']} -> {C.FAIL}{item['to']}{C.END}"
            elif item["from"] in exchanges:
                # highlight source yellow for exchanges
                flow_colored = f"{C.WARNING}{item['from']}{C.END} -> {item['to']}"
            else:
                flow_colored = flow_vis

            pad_flow = " " * (35 - len(flow_vis))

            # format time column
            time_str = f"{item['time']:<10}"

            # combine all parts and print aligned row
            row = f"   {colored_asset}{pad_asset}{amount_str}{colored_val}{pad_val}{flow_colored}{pad_flow}{time_str}"
            print(row)

        input(f"\n{ui['return_msg']}")

    def show_gas_tracker(self, current_lang, user_label, base_path):
        # monitors gas fees across networks using manual alignment
        title = "GAZ ÜCRETİ TAKİPÇİSİ" if current_lang == "tr" else "GAS FEE TRACKER"
        MenuV2.prepare_content_screen(base_path + [title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_gas_data(current_lang)

        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'AĞ':<15}{'GWEI':<10}{'TRANSFER':<15}{'SWAP':<15}{'DURUM':<15}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'NETWORK':<15}{'GWEI':<10}{'TRANSFER':<15}{'SWAP':<15}{'STATUS':<15}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 70}{C.END}")

        for item in data:
            net = f"{item['network']:<15}"
            gwei = f"{str(item['gwei']):<10}"
            trans = f"${item['transfer']:<15}"
            swap = f"${item['swap']:<15}"
            icon = "🟢" if item["status_code"] == "LOW" else ("🔴" if item["status_code"] == "HIGH" else "🟡")
            color = C.GREEN if item["status_code"] == "LOW" else (
                C.FAIL if item["status_code"] == "HIGH" else C.WARNING)
            stat_vis = f"{icon} {item['status']}"
            stat_str = f"{color}{stat_vis}{C.END}" + (" " * (15 - len(stat_vis)))
            print(f"   {net}{gwei}{trans}{swap}{stat_str}")

        input(f"\n{ui['return_msg']}")

    def view_economic_calendar(self, current_lang, user_label, base_path):
        # lists global economic events with specialized manual padding
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
            raw_event = item['event']
            if len(raw_event) > 30: raw_event = raw_event[:28] + ".."
            event_str = f"{C.BOLD}{raw_event}{C.END}" + (" " * (32 - len(raw_event)))

            icon = "🔥" if item["impact"] == "high" else ("🔸" if item["impact"] == "med" else "🔹")
            color = C.FAIL if item["impact"] == "high" else (C.WARNING if item["impact"] == "med" else C.GREY)
            impact_vis = f"{icon} {item['impact_label']}"
            impact_str = f"{color}{impact_vis}{C.END}" + (" " * (18 - len(impact_vis) - 1))
            stats_vis = f"{item['prev']} / {item['forecast']}"
            stats_str = f"{item['prev']} / {C.CYAN}{item['forecast']}{C.END}" + (" " * (20 - len(stats_vis)))

            print(f"   {item['time']:<8}{item['currency']:<6}{event_str}{impact_str}{stats_str}")

        input(f"\n{ui['return_msg']}")

    def show_ico_calendar(self, current_lang, user_label, base_path):
        # existing list code remains same until choice logic
        # ... fetch data and print table ...

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_ico_list(current_lang)

        # print project table header
        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'PROJE':<15}{'TÜR':<12}{'KATEGORİ':<15}{'DURUM':<12}{'HEDEF':<10}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'PROJECT':<15}{'TYPE':<12}{'CATEGORY':<15}{'STATUS':<12}{'GOAL':<10}{C.END}"
        print(h_str)
        print("   " + f"{C.GREY}{'-' * 70}{C.END}")

        for item in data:
            idx = f"{item['id']:<4}"
            name = f"{C.BOLD}{item['name']:<15}{C.END}"
            type_str = f"{item['type']:<12}"
            cat = f"{item['cat']:<15}"
            status_val = item['status']
            color = C.GREEN if status_val in ["Active", "Aktif", "Testnet"] else C.WARNING
            status_str = f"{color}{status_val}{C.END}" + (" " * (12 - len(status_val)))
            goal = f"{item['goal']:<10}"
            print(f"   {idx}{name}{type_str}{cat}{status_str}{goal}")

        print(f"\n   [{C.FAIL}0{C.END}] " + ("İptal" if current_lang == "tr" else "Cancel"))
        print(f"\n{ui['input_prefix']}{ui['select_asset']}", end="")
        choice = input().strip()

        if choice.isdigit() and 1 <= int(choice) <= len(data):
            selected = data[int(choice) - 1]
            details = self.market_service.get_ico_details(selected['id'], current_lang)

            # clear screen for high quality detailed report
            MenuV2.prepare_content_screen(base_path + ["DETAILS", selected['name']], user_info=user_label)

            # localized field labels
            l = {
                "tr": ["PROJE RAPORU", "Açıklama", "Platform", "Kilit Yapısı", "Yatırımcılar", "Kullanım",
                       "Risk Skoru"],
                "en": ["PROJECT REPORT", "Description", "Platform", "Lock Structure", "Top Investors", "Utility",
                       "Risk Score"]
            }[current_lang]

            print(f"   {C.CYAN}{C.BOLD}{l[0]}: {selected['name'].upper()}{C.END}")
            print(f"   {C.GREY}{'━' * 60}{C.END}")

            # print formatted data rows
            print(f"   {C.BOLD}{l[1]:<15}:{C.END} {details['desc']}")
            print(f"   {C.BOLD}{l[2]:<15}:{C.END} {details['platform']}")
            print(f"   {C.BOLD}{l[3]:<15}:{C.END} {details['lock']}")
            print(f"   {C.BOLD}{l[4]:<15}:{C.END} {C.GREEN}{details['investors']}{C.END}")
            print(f"   {C.BOLD}{l[5]:<15}:{C.END} {details['utility']}")

            # risk color logic
            r_val = details['risk']
            r_color = C.FAIL if "High" in r_val or "Yüksek" in r_val else C.GREEN
            print(f"   {C.BOLD}{l[6]:<15}:{C.END} {r_color}{r_val}{C.END}")

            print(f"   {C.GREY}{'━' * 60}{C.END}")
            input(f"\n   {ui['return_msg']}")

    def show_token_unlocks(self, current_lang, user_label, base_path):
        # prepare screen and fetch unlock data
        t_title = "TOKEN KİLİT AÇILIMLARI" if current_lang == "tr" else "TOKEN UNLOCKS"
        MenuV2.prepare_content_screen(base_path + [t_title], user_info=user_label)

        ui = self._get_ui_strings(current_lang)
        data = self.market_service.get_unlock_list(current_lang)

        # print header with manual alignment
        if current_lang == "tr":
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'VARLIK':<12}{'TARİH':<15}{'MİKTAR':<12}{'DEĞER':<12}{'ORAN':<8}{C.END}"
        else:
            h_str = f"   {C.BOLD}{C.CYAN}{'#':<4}{'ASSET':<12}{'DATE':<15}{'AMOUNT':<12}{'VALUE':<12}{'RATIO':<8}{C.END}"

        print(h_str)
        print("   " + f"{C.GREY}{'-' * 65}{C.END}")

        # render list of unlock events
        for item in data:
            idx = f"{item['id']:<4}"
            asset = f"{C.BOLD}{item['symbol']:<12}{C.END}"
            date = f"{item['date']:<15}"
            amount = f"{item['amount']:<12}"
            val = f"{C.CYAN}{item['value']:<12}{C.END}"

            # highlight ratio if it's high impact
            ratio_val = item['ratio']
            r_color = C.FAIL if float(ratio_val.replace('%', '')) > 2.0 else C.GREY
            ratio_str = f"{r_color}{ratio_val:<8}{C.END}"

            print(f"   {idx}{asset}{date}{amount}{val}{ratio_str}")

        print(f"\n   [{C.FAIL}0{C.END}] " + ("Geri" if current_lang == "tr" else "Back"))
        print(f"\n{ui['input_prefix']}{ui['select_asset']}", end="")
        choice = input().strip()

        if choice.isdigit() and 1 <= int(choice) <= len(data):
            selected = data[int(choice) - 1]
            details = self.market_service.get_unlock_details(selected['id'], current_lang)

            # clear screen for distribution report
            MenuV2.prepare_content_screen(base_path + [t_title, selected['symbol']], user_info=user_label)

            head = "DAĞITIM DETAYLARI" if current_lang == "tr" else "DISTRIBUTION DETAILS"
            print(f"   {C.BOLD}{head}: {C.CYAN}{selected['name']} ({selected['symbol']}){C.END}")
            print(f"   {C.GREY}{'━' * 55}{C.END}\n")

            # render simple bar chart for allocations
            for row in details["breakdown"]:
                label = f"{row['label']:<20}"
                pct = row['val']
                bar_len = int(float(pct.replace('%', '')) / 100 * 30)
                bar = f"{C.GREEN}{'█' * bar_len}{C.GREY}{'░' * (30 - bar_len)}{C.END}"
                print(f"   {label} {bar} {C.BOLD}{pct}{C.END}")

            print(f"\n   {C.GREY}{'━' * 55}{C.END}")
            input(f"\n   {ui['return_msg']}")