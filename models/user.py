class User:
    def __init__(self, username, password, balance=10000.0):
        self.username = username
        self.password = password
        self.balance = balance
        self.assets = {}  # Örn: {'BTC': 0.1}
        self.history = [] # YENİ: İşlem geçmişi listesi

    def __str__(self):
        return f"User: {self.username} | Balance: {self.balance} USDT"