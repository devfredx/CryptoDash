# 🚀 CryptoDash: Terminal-Based Crypto Trading Simulator
**Version:** `1.0.0 (Stable Release)`

CryptoDash is a robust, console-based cryptocurrency trading simulator built with Python. It provides a realistic environment for users to track markets, manage portfolios, and execute trades without financial risk.

---

## ✨ Key Features (v1.0)
- **🔐 Secure Authentication:** User registration and login system with persistent data storage.
- **💹 Market Simulation:** Real-time tracking of popular crypto assets (BTC, ETH, SOL, etc.).
- **💰 Dynamic Wallet:** Automated portfolio value calculation based on current market prices.
- **🔄 Trade Engine:** Seamless "Buy" and "Sell" logic with instant balance updates.
- **📊 Transaction History:** Detailed logs for every trade, including dates, prices, and amounts.
- **🌍 Multilingual Support:** Fully functional interface in both **Turkish** and **English**.
- **📰 Integrated News & Support:** Live-feed simulation for crypto headlines and a dedicated FAQ/Support section.
- **💾 Data Persistence:** All user data, balances, and histories are securely saved and loaded from `users.json`.

---

## 🛠 Tech Stack
- **Language:** Python 3.x
- **Storage:** JSON (Local File System)
- **Architecture:** Layered Service-Repository Pattern

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed on your system.

### Installation & Execution
1. Clone or download the repository to your local machine.
2. Open your terminal or IDE (PyCharm/IntelliJ).
3. Navigate to the project directory:
   ```bash
   cd CryptoDash
   ```

## Run the application:
 ```bash
   python main.py
   ```

## 📂 Project Structure
```bash
CryptoDash/
├── models/         # Data blueprints (User, Asset)
├── repository/     # Data persistence logic (JSON handling)
├── service/        # Business logic (Auth, Trade, Market, News, Support)
├── ui/             # Terminal interface and strings (Localization)
├── users.json      # Local database (Generated automatically)
└── main.py         # Application entry point
```

## 🗺 Roadmap (Future Goals)

[ ] 🚀 Feature Expansion: Development of an enriched suite of functionalities and advanced trading tools to broaden the application's capabilities.

[ ] 💾 Enhanced Data Persistence: Implementation of more robust and secure long-term storage solutions for user profiles and transaction records.

[ ] 🎨 UI/UX Optimization: Transitioning to a more intuitive, user-centric interface and refined experience to elevate overall usability.

## 👤 Author
Ferhat Susam

Project Phase: V1.0 Complete

Last Updated: 31/01/2026


Disclaimer: This is a simulation tool. No real currency is used or traded.

Happy Trading!