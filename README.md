# Trade Analyzer

Python tool to analyze TradingView signal logs versus Tradovate execution data, compute slippage, and visualize P\&L performance by instrument and strategy.

## 🚀 Project Goals

* Import signals from TradingView and execution data from Tradovate
* Match signals with fills to compute per-trade slippage
* Calculate profit/loss by trade, session, and instrument
* Visualize equity curves, drawdowns, and slippage distributions
* Export reports suitable for self-analysis and broker verification

## 📁 Project Structure

```
trade_analyzer/
├── data/              # Importing and normalizing signal/fill data
├── models/            # Core data models (signals, trades, sessions)
├── logic/             # Matching and slippage computation
├── reports/           # P&L summaries, exports, performance metrics
├── ui/                # Optional Streamlit dashboard (Sprint 4)
├── tests/             # Unit and integration tests
├── utils/             # Time conversion and misc utilities
├── main.py            # CLI entrypoint
├── README.md          # This file
├── requirements.txt   # Python dependencies
├── .gitignore         # Ignored files and folders
└── .env               # API keys or secrets (excluded from Git)
```

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/trade_analyzer.git
cd trade_analyzer
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables (Optional)

If using the Tradovate API, create a `.env` file:

```
TRADOVATE_CLIENT_ID=your_client_id
TRADOVATE_CLIENT_SECRET=your_secret
```

### 5. Run the Analyzer (Once Developed)

```bash
python main.py
```

Or run the Streamlit dashboard (once built):

```bash
streamlit run ui/streamlit_app.py
```

## 📅 Sprint Roadmap

See `Trade Analyzer Requirements.md` for detailed sprint planning and use cases.

---

MIT License © 2025 Your Name
