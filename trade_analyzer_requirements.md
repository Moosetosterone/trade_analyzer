

## **📋 Requirements Document: TradingView + Tradovate Paper Trade Analyzer**

### **🧩 Purpose**

To create a Python-based analytics tool that allows a trader to:

- Import **strategy signal logs** from TradingView (via CSV or JSON exports).
- Import **order execution logs** from Tradovate (via CSV, API, or webhook logs).
- Compare signal vs. execution timing and price.
- Compute **slippage** (price difference between signal and execution).
- Compute **profit/loss** by instrument, time range, or strategy.
- Visualize P&L over time, by strategy, and slippage statistics.

## **✅ Functional Requirements**

### \*\*1. \*\***Data Ingestion**

- Import TradingView signal logs (JSON or CSV).
- Import Tradovate execution logs (JSON, CSV, or API).
- Timestamp synchronization and timezone normalization.
- Instrument symbol normalization (e.g., MES1! vs MESM25).



### \*\*2. \*\***Trade Matching Engine**

- Match signals (TradingView) to fills (Tradovate) by:

  - Instrument
  - Trade direction (long/short)
  - Signal time vs. execution time (e.g., within ±2 minutes)

- Flag unmatched signals or fills.



### \*\*3. \*\***Slippage Analysis**

- Compute per-trade slippage (in ticks and dollars).

- Aggregate slippage by:

  - Instrument
  - Time of day
  - Strategy
  - Trade direction

- Visualize slippage distribution (histogram, box plot).



### \*\*4. \*\***P&L Analysis**

- Compute per-trade, per-day, per-instrument P&L.

- Include customizable commission/slippage assumptions.

- Allow for grouping by:

  - Instrument
  - Session (Asia, London, NY)
  - Strategy

- Visualize equity curve and drawdowns.



### \*\*5. \*\***Exports & Reports**

- Export trade history with matched signal + fill info.
- Export summary reports (PDF, CSV).
- Summary tables: win rate, avg P&L, total trades, expectancy.



## **🔁 Use Cases**

### **UC1: “Analyze Strategy Slippage”**

**Actor:** Trader

**Goal:** Determine how much slippage occurs between the TradingView signal and the Tradovate execution

**Steps:**

1. Load logs from TradingView and Tradovate
2. Run trade matching algorithm
3. Output slippage stats (avg, max, by instrument)



### **UC2: “Daily P&L Summary”**

**Actor:** Trader

**Goal:** Review total profits/losses by day, strategy, and instrument

**Steps:**

1. Import fill data
2. Aggregate trades by date
3. Generate summary tables and equity curve plots



### **UC3: “Compare Strategy Results”**

**Actor:** Developer

**Goal:** Backtest multiple versions of a TradingView strategy and compare live execution differences

**Steps:**

1. Import multiple signal logs
2. Match against fills
3. Compare expected P&L vs. actual



### **UC4: “Export Broker-Ready Report”**

**Actor:** Trader

**Goal:** Show a prop firm or investor a verified trade log

**Steps:**

1. Load logs
2. Filter by instrument and date range
3. Export formatted PDF with metrics and notes



## **📦 Planned Features (v1 Roadmap)**

- CLI or Streamlit UI
- JSON/CSV importers for both platforms
- SQLite or in-memory Pandas data model
- Trade matcher (with tolerance window setting)
- Summary table: P&L, win rate, slippage
- Matplotlib/Plotly charts: equity curve, slippage dist
- PDF/CSV export options





## **🗂 Sprint Planning**

I recommend using 2-week sprints. Here’s a suggested 4-sprint roadmap to get from prototype to MVP:

### **🌀 Sprint 1: Data Infrastructure & Input**

**Goal:** Build the ingestion and storage pipeline.

#### **Tasks**

- Define data schemas for:

  - TradingView signals (timestamp, symbol, direction, signal\_price, etc.)
  - Tradovate fills (timestamp, symbol, fill\_price, qty, direction, etc.)

- Implement CSV/JSON import functions

- Normalize timestamps and timezones

- Normalize instrument naming (e.g., MES1! → MESM25)

- Store data in in-memory or SQLite (Pandas-based)



### **🌀 Sprint 2: Trade Matching & Slippage**

**Goal:** Match signal and execution data to calculate slippage.

#### **Tasks**

- Implement matching logic (configurable time window, instrument, direction)
- Flag unmatched signals/fills
- Compute per-trade slippage in ticks and dollars
- Aggregate and summarize slippage stats
- Unit tests for matcher



### **🌀 Sprint 3: P&L Computation & Reporting**

**Goal:** Build profit/loss computation and reporting tools.

#### **Tasks**

- Compute per-trade and per-day P&L
- Allow grouping by instrument, strategy, session
- Add commission/slippage assumptions
- Generate summary tables (win rate, expectancy, drawdown)
- Export summary as CSV



### **🌀 Sprint 4: Visualization & UI**

**Goal:** Build basic UI and visual output for usability.

#### **Tasks**

- Plot equity curve (cumulative P&L)
- Visualize slippage distribution (histogram, box plot)
- Implement Streamlit or CLI interface
- Export broker-ready PDF report


# Trade Analyzer

A modular Python project for ingesting, normalizing, matching, and analyzing trading signals and execution fills. Follows SOLID design principles to ensure maintainability and extensibility.

## 📂 Project Structure

```
trade_analyzer/
├── data/
│   ├── schemas.py             # Pydantic models for signals and fills
│   ├── normalizer.py          # CSV row → model factories, timezone & format handling
│   ├── importer.py            # CSV import pipelines for signals and fills
│   ├── instrument_normalizer.py # Ticker normalization (external YAML config)
│   ├── matching.py            # MatchingEngine + MatchRecord
│   ├── pipeline.py            # run_matching_pipeline & run_full_pipeline (unmatched)
│   ├── db.py                  # SQLite persistence (SQLModel) and upsert helpers
│   ├── analytics.py           # SlippageRecord, compute_slippage, aggregate_slippage
│   ├── pnl.py                 # PnLRecord, compute_trade_pnl, aggregate_daily_pnl
│   ├── grouping.py            # Generic/group-by/filter utilities
│   ├── summary.py             # Win rate, expectancy, equity curve, drawdown
│   └── export.py              # CSV export utilities
├── config/
│   └── instrument_mapping.yaml # Overrides, month codes, rollover rules
├── tests/                     # pytest suite covering all modules
│   ├── test_tradingview_signal_factory.py
│   ├── test_instrument_normalizer.py
│   ├── test_matching_engine.py
│   ├── test_pipeline.py
│   ├── test_db.py
│   ├── test_analytics.py
│   ├── test_pnl.py
│   ├── test_grouping.py
│   ├── test_summary.py
│   └── test_export.py
├── data/                      # sample CSV files
│   ├── TradingView_Alerts_Log_2025-07-03_790cd.csv
│   └── Orders-4.csv
├── pyproject.toml
└── README.md
```

## ✅ SOLID Adherence

* **Single Responsibility**: Each module/class has one purpose (e.g., normalization vs. persistence).
* **Open/Closed**: Factories and normalizers can be extended via config files without touching core schemas.
* **Liskov Substitution**: Interfaces (functions/classes) accept base types (`MatchRecord`, `PnLRecord`) that can be replaced.
* **Interface Segregation**: Consumers import only what they need (e.g., `compute_slippage` without DB code).
* **Dependency Inversion**: High-level pipelines orchestrate factories, matching, persistence without hardcoding implementations.

## 📝 Documentation Guidelines

* Use **Google-style docstrings** for modules, classes, and functions. See [Real Python](https://realpython.com/documenting-python-code/).
* Include **`Args:`** and **`Returns:`** sections.
* Document edge cases & date/time formats in docstrings.
* Maintain documentation close to code; update README for high-level overviews.

### Example Docstring

```python
def compute_slippage(
    record: MatchRecord,
    tick_size: float,
    tick_value: float
) -> SlippageRecord:
    """
    Compute slippage for a matched signal and fill.

    Args:
        record: MatchRecord tying signal and fill.
        tick_size: Price increment per tick (e.g., 0.25).
        tick_value: Dollar value per tick (e.g., 12.5).

    Returns:
        SlippageRecord: Contains slippage in ticks and dollars.
    """
    ...
```

## 🚀 Getting Started

1. **Install** dependencies: `pip install -r requirements.txt` (includes SQLModel, pydantic)
2. **Run tests**: `pytest tests/`
3. **Ingest & match**:

   ```bash
   python -m data.pipeline data/TradingView_Alerts_Log.csv data/Orders-4.csv
   ```
4. **Analyze & export**:

   ```python
   from data.pipeline import run_full_pipeline
   from data.pnl import compute_trade_pnl
   from data.summary import equity_curve
   from data.export import export_pnl_records

   matches, unmatch_sigs, unmatch_fills = run_full_pipeline(...)
   pnl_records = [compute_trade_pnl(m) for m in matches]
   export_pnl_records(pnl_records, 'pnl.csv')
   curve = equity_curve(pnl_records)
   ```

## 📚 Next Steps (Sprint 4)

* **Dashboard**: Streamlit or Plotly for interactive equity and slippage charts.
* **Drawdown reports**: Visualize historical drawdowns.
* **Strategy tags**: Add strategy metadata & grouping.
* **CI/CD**: Integrate linting, coverage, and docs generation.
