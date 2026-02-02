# ui/menu_map.py

def get_guest_menu_structure(lang="en"):
    # define labels for supported languages
    labels = {
        "en": {
            "m1": "MARKETS",
            "m1_items": ["Market Data", "Analysis Tools", "Calendars"],
            "m2": "TRADE",
            "m2_items": ["Trade Ops", "Simulation", "Earn & Borrow"],
            "m3": "DISCOVER",
            "m3_items": ["News", "Announcements", "Research", "Reports", "Academy"],
            "m4": "COMPANY",
            "m4_items": ["About Us", "Team", "Partners", "Sitemap"],
            "m5": "SUPPORT",
            "m5_items": ["Help (FAQ)", "Legal", "Fees", "Risk Notice"],
            "m6": "ACCOUNT",
            "m6_items": ["🔍 Search", "🌐 Lang (EN/TR)", "🔑 Login", "📝 Register"],
            "back": "Main Menu"
        },
        "tr": {
            "m1": "PIYASALAR",
            "m1_items": ["Piyasa Verileri", "Analiz Araçları", "Takvimler"],
            "m2": "AL-SAT",
            "m2_items": ["İşlemler", "Simülasyon", "Kazan & Borçlan"],
            "m3": "KESFET",
            "m3_items": ["Haberler", "Duyurular", "Araştırmalar", "Raporlar", "Akademi"],
            "m4": "KURUMSAL",
            "m4_items": ["Hakkımızda", "Yönetim Ekibi", "İş Ortakları", "Site Haritası"],
            "m5": "DESTEK",
            "m5_items": ["Yardım (SSS)", "Yasal", "Ücretler", "Risk Bildirimi"],
            "m6": "HESAP",
            "m6_items": ["🔍 Arama", "🌐 Dil (TR/EN)", "🔑 Giriş", "📝 Kayıt"],
            "back": "Ana Menü"
        }
    }

    # select text based on current language
    txt = labels.get(lang, labels["en"])

    # build the mega menu tree
    menu_tree = {
        "1": {"title": txt["m1"], "goto": "markets", "preview": txt["m1_items"]},
        "2": {"title": txt["m2"], "goto": "trade", "preview": txt["m2_items"]},
        "3": {"title": txt["m3"], "goto": "discover", "preview": txt["m3_items"]},
        "4": {"title": txt["m4"], "goto": "company", "preview": txt["m4_items"]},
        "5": {"title": txt["m5"], "goto": "support", "preview": txt["m5_items"]},
        "6": {"title": txt["m6"], "goto": "account", "preview": txt["m6_items"]}
    }

    # define sub menu actions and labels
    # using english keys for logic but localized labels for display
    sub_menus = {
        "markets": {
            "title": txt["m1"],
            "options": {
                "1": {"label": txt["m1_items"][0], "action": "market_data"},
                "2": {"label": txt["m1_items"][1], "action": "analysis"},
                "3": {"label": txt["m1_items"][2], "action": "calendars"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "trade": {
            "title": txt["m2"],
            "options": {
                "1": {"label": txt["m2_items"][0], "action": "trade_ops"},
                "2": {"label": txt["m2_items"][1], "action": "simulation"},
                "3": {"label": txt["m2_items"][2], "action": "earn"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "discover": {
            "title": txt["m3"],
            "options": {
                "1": {"label": txt["m3_items"][0], "action": "news"},
                "2": {"label": txt["m3_items"][1], "action": "reports"},
                "3": {"label": txt["m3_items"][4], "action": "academy"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "company": {
            "title": txt["m4"],
            "options": {
                "1": {"label": txt["m4_items"][0], "action": "about"},
                "2": {"label": txt["m4_items"][1], "action": "team"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "support": {
            "title": txt["m5"],
            "options": {
                "1": {"label": txt["m5_items"][0], "action": "faq"},
                "2": {"label": txt["m5_items"][1], "action": "legal"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        },
        "account": {
            "title": txt["m6"],
            "options": {
                "L": {"label": txt["m6_items"][2], "action": "login"},
                "R": {"label": txt["m6_items"][3], "action": "register"},
                "S": {"label": txt["m6_items"][0], "action": "search"},
                "D": {"label": txt["m6_items"][1], "action": "lang"},
                "0": {"label": txt["back"], "action": "GO_BACK"}
            }
        }
    }

    return menu_tree, sub_menus