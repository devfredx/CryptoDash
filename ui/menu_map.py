# ui/menu_map.py

def get_guest_menu_structure(lang="en"):
    # define labels
    labels = {
        "en": {
            # dashboard headers
            "m1": "MARKETS",
            "m2": "TRADE",
            "m3": "DISCOVER",
            "m4": "COMPANY",
            "m5": "SUPPORT",
            "m6": "ACCOUNT",

            # level 2 previews
            "m1_cats": ["Market Data", "Analysis Tools", "Calendars"],
            "m2_cats": ["Trading", "Simulation", "Earn & Borrow"],
            "m3_cats": ["News", "Announcements", "Research", "Reports", "Academy"],
            "m4_cats": ["About Us", "Team", "Partners", "Sitemap"],
            "m5_cats": ["FAQ", "Contact", "Fees", "Risk Notice"],
            # column 6 has emojis
            "m6_cats": ["🔍 Search", "🌐 Language", "🔑 Login", "📝 Register"],

            # level 3 detailed items
            "md_items": ["Crypto Prices", "New Listings", "Gainers/Losers", "Sectors (DeFi/AI)", "Fear & Greed Index"],
            "ma_items": ["TradingView Chart", "Heatmap", "On-Chain Data", "Whale Alert", "Gas Fee Heatmap"],
            "mc_items": ["Economic Calendar", "Airdrop & ICO", "Token Unlocks"],

            "to_items": ["Swap (Easy Buy/Sell)", "Spot Market", "Convert"],
            "ts_items": ["Paper Trading", "Virtual Portfolio"],
            "te_items": ["Earn / Staking", "Crypto Loans"],

            "langs": ["🇺🇸 English", "🇹🇷 Türkçe", "🇩🇪 Deutsch", "🇪🇸 Español", "🇷🇺 Русский", "🇨🇳 Chinese (Zh)"],

            "back": "Go Back"
        },
        "tr": {
            "m1": "PIYASALAR",
            "m2": "AL-SAT",
            "m3": "KESFET",
            "m4": "KURUMSAL",
            "m5": "DESTEK",
            "m6": "HESAP",

            "m1_cats": ["Piyasa Verileri", "Analiz Araçları", "Takvimler"],
            "m2_cats": ["İşlemler", "Simülasyon", "Kazan & Borçlan"],
            "m3_cats": ["Haberler", "Duyurular", "Araştırmalar", "Raporlar", "Akademi"],
            "m4_cats": ["Hakkımızda", "Yönetim Ekibi", "İş Ortakları", "Site Haritası"],
            "m5_cats": ["SSS", "İletişim", "Ücretler", "Risk Bildirimi"],
            # column 6 has emojis
            "m6_cats": ["🔍 Arama", "🌐 Dil", "🔑 Giriş", "📝 Kayıt"],

            "md_items": ["Kripto Fiyatları", "Yeni Listelenenler", "Kazananlar/Kaybedenler", "Sektörler (DeFi/AI)", "Korku & Açgözlülük"],
            "ma_items": ["Gelişmiş Grafik", "Sıcaklık Haritası", "Zincir Üstü Veriler", "Balina Hareketleri", "Gas Fee Heatmap"],
            "mc_items": ["Ekonomik Takvim", "Airdrop & ICO", "Token Kilit Açılımı"],

            "to_items": ["Kolay Al/Sat", "Spot Borsa", "Hızlı Dönüştür"],
            "ts_items": ["Demo İşlem", "Sanal Portföy"],
            "te_items": ["Kazan (Staking)", "Kripto Krediler"],

            "langs": ["🇺🇸 English", "🇹🇷 Türkçe", "🇩🇪 Deutsch", "🇪🇸 Español", "🇷🇺 Русский", "🇨🇳 Çince (Zh)"],

            "back": "Geri Dön"
        }
    }

    txt = labels.get(lang, labels["en"])

    # mega menu tree
    menu_tree = {
        "1": {"title": txt["m1"], "goto": "markets", "preview": txt["m1_cats"]},
        "2": {"title": txt["m2"], "goto": "trade",   "preview": txt["m2_cats"]},
        "3": {"title": txt["m3"], "goto": "discover", "preview": txt["m3_cats"]},
        "4": {"title": txt["m4"], "goto": "company",  "preview": txt["m4_cats"]},
        "5": {"title": txt["m5"], "goto": "support",  "preview": txt["m5_cats"]},
        "6": {"title": txt["m6"], "goto": "account",  "preview": txt["m6_cats"]}
    }

    # sub menus
    sub_menus = {
        # level 2 router menus
        "markets": {
            "title": txt["m1"],
            "options": {
                "1": {"label": txt["m1_cats"][0], "action": "NAV_MARKET_DATA"},
                "2": {"label": txt["m1_cats"][1], "action": "NAV_MARKET_ANALYSIS"},
                "3": {"label": txt["m1_cats"][2], "action": "NAV_MARKET_CALENDAR"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "trade": {
            "title": txt["m2"],
            "options": {
                "1": {"label": txt["m2_cats"][0], "action": "NAV_TRADE_OPS"},
                "2": {"label": txt["m2_cats"][1], "action": "NAV_TRADE_SIM"},
                "3": {"label": txt["m2_cats"][2], "action": "NAV_TRADE_EARN"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },

        # level 3 market details
        "market_data": {
            "title": txt["m1_cats"][0].upper(),
            "options": {
                "1": {"label": txt["md_items"][0], "action": "view_prices"},
                "2": {"label": txt["md_items"][1], "action": "view_listings"},
                "3": {"label": txt["md_items"][2], "action": "view_gainers"},
                "4": {"label": txt["md_items"][3], "action": "view_sectors"},
                "5": {"label": txt["md_items"][4], "action": "view_fear_greed"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "market_analysis": {
            "title": txt["m1_cats"][1].upper(),
            "options": {
                "1": {"label": txt["ma_items"][0], "action": "show_chart"},
                "2": {"label": txt["ma_items"][1], "action": "show_heatmap"},
                "3": {"label": txt["ma_items"][2], "action": "show_onchain"},
                "4": {"label": txt["ma_items"][3], "action": "show_whale_alert"},
                "5": {"label": txt["ma_items"][4], "action": "show_gas"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "market_calendar": {
            "title": txt["m1_cats"][2].upper(),
            "options": {
                "1": {"label": txt["mc_items"][0], "action": "show_eco_cal"},
                "2": {"label": txt["mc_items"][1], "action": "show_ico"},
                "3": {"label": txt["mc_items"][2], "action": "show_unlocks"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },

        # level 3 trade details
        "trade_ops": {
            "title": txt["m2_cats"][0].upper(),
            "options": {
                "1": {"label": txt["to_items"][0], "action": "trade_swap"},
                "2": {"label": txt["to_items"][1], "action": "trade_spot"},
                "3": {"label": txt["to_items"][2], "action": "trade_convert"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "trade_sim": {
            "title": txt["m2_cats"][1].upper(),
            "options": {
                "1": {"label": txt["ts_items"][0], "action": "sim_paper"},
                "2": {"label": txt["ts_items"][1], "action": "sim_portfolio"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "trade_earn": {
            "title": txt["m2_cats"][2].upper(),
            "options": {
                "1": {"label": txt["te_items"][0], "action": "earn_staking"},
                "2": {"label": txt["te_items"][1], "action": "earn_loans"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },

        # standard columns
        "discover": {
            "title": txt["m3"],
            "options": {
                "1": {"label": txt["m3_cats"][0], "action": "news"},
                "2": {"label": txt["m3_cats"][1], "action": "announcements"},
                "3": {"label": txt["m3_cats"][2], "action": "research"},
                "4": {"label": txt["m3_cats"][3], "action": "reports"},
                "5": {"label": txt["m3_cats"][4], "action": "academy"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "company": {
            "title": txt["m4"],
            "options": {
                "1": {"label": txt["m4_cats"][0], "action": "about"},
                "2": {"label": txt["m4_cats"][1], "action": "team"},
                "3": {"label": txt["m4_cats"][2], "action": "partners"},
                "4": {"label": txt["m4_cats"][3], "action": "sitemap"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "support": {
            "title": txt["m5"],
            "options": {
                "1": {"label": txt["m5_cats"][0], "action": "faq"},
                "2": {"label": txt["m5_cats"][1], "action": "contact"},
                "3": {"label": txt["m5_cats"][2], "action": "fees"},
                "4": {"label": txt["m5_cats"][3], "action": "risk_notice"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },

        # account menu
        "account": {
            "title": txt["m6"],
            "options": {
                "1": {"label": txt["m6_cats"][0], "action": "search"},
                "2": {"label": txt["m6_cats"][1], "action": "NAV_LANGUAGE_SELECT"},
                "3": {"label": txt["m6_cats"][2], "action": "login"},
                "4": {"label": txt["m6_cats"][3], "action": "register"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },

        # language menu
        "language_select": {
            "title": "SELECT LANGUAGE / DİL SEÇİMİ",
            "options": {
                "1": {"label": txt["langs"][0], "action": "set_lang_en"},
                "2": {"label": txt["langs"][1], "action": "set_lang_tr"},
                "3": {"label": txt["langs"][2], "action": "set_lang_de"},
                "4": {"label": txt["langs"][3], "action": "set_lang_es"},
                "5": {"label": txt["langs"][4], "action": "set_lang_ru"},
                "6": {"label": txt["langs"][5], "action": "set_lang_zh"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        }
    }

    return menu_tree, sub_menus