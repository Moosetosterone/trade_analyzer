# ui/streamlit_app.py
import os
import sys

# Ensure the project root (one level up) is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tempfile

import streamlit as st

from analytics.pnl import compute_trade_pnl
from analytics.summary import equity_curve
from analytics.visualization import (
    plot_equity_and_drawdown,
    plot_equity_curve,
    plot_slippage_histogram,
)
from ingestion.pipeline import run_full_pipeline

st.set_page_config(page_title="Trade Analyzer", layout="wide")
st.title("Trade Analyzer Dashboard")

# Sidebar: file uploaders and filters
st.sidebar.header("Data Upload")
tv_file = st.sidebar.file_uploader("TradingView Alerts CSV", type=["csv"])
fills_file = st.sidebar.file_uploader("Tradovate Fills CSV", type=["csv"])

if tv_file and fills_file:
    tolerance = st.sidebar.number_input(
        "Matching tolerance (minutes)", min_value=0, value=2
    )
    date_filter = st.sidebar.date_input("Date range filter", [])

    # Save uploaded files to temp files on disk
    tv_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    fills_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    try:
        tv_tmp.write(tv_file.read())
        tv_tmp.flush()
        fills_tmp.write(fills_file.read())
        fills_tmp.flush()

        # Run the end-to-end pipeline
        matches, unmatched_signals, unmatched_fills = run_full_pipeline(
            tv_tmp.name, fills_tmp.name, tolerance_min=tolerance
        )
    finally:
        # Clean up temp files
        tv_tmp.close()
        os.unlink(tv_tmp.name)
        fills_tmp.close()
        os.unlink(fills_tmp.name)

    # Compute PnL records for matched trades
    pnl_records = [compute_trade_pnl(m) for m in matches]

    # Apply optional date range filter to PnL records and unmatched lists
    if len(date_filter) == 2:
        start_date, end_date = date_filter
        pnl_records = [r for r in pnl_records if start_date <= r.date <= end_date]
        unmatched_signals = [
            s for s in unmatched_signals if start_date <= s.timestamp.date() <= end_date
        ]
        unmatched_fills = [
            f for f in unmatched_fills if start_date <= f.timestamp.date() <= end_date
        ]

    # Instrument multi-select and filtering for PnL and unmatched lists
    instruments = sorted({r.symbol for r in pnl_records})
    selected_instruments = st.sidebar.multiselect(
        "Filter by instrument", instruments, default=instruments
    )
    pnl_records = [r for r in pnl_records if r.symbol in selected_instruments]
    unmatched_signals = [
        s for s in unmatched_signals if s.symbol in selected_instruments
    ]
    unmatched_fills = [f for f in unmatched_fills if f.contract in selected_instruments]

    # ───── Overview Metrics ───────────────────────────────────────────────────────────
    total_trades = len(pnl_records)
    gross = sum(r.gross_pnl for r in pnl_records)
    net = sum(r.net_pnl for r in pnl_records)
    wins = [r for r in pnl_records if r.gross_pnl > 0]
    losses = [r for r in pnl_records if r.gross_pnl < 0]
    win_rate = (len(wins) / total_trades * 100) if total_trades else 0.0
    profit_factor = (
        (sum(r.gross_pnl for r in wins) / abs(sum(r.gross_pnl for r in losses)))
        if losses
        else float("inf")
    )
    # max drawdown
    curve = equity_curve(pnl_records)
    values = [v for (_d, v) in curve]
    peak, max_dd = float("-inf"), 0.0
    for x in values:
        peak = max(peak, x)
        max_dd = min(max_dd, x - peak)
    max_dd = abs(max_dd)

    st.subheader("Overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Trades", f"{total_trades}")
    c2.metric("Total P&L", f"${net:,.2f}", f"${(net - gross):,.2f}")
    c3.metric("Max Drawdown", f"${max_dd:,.2f}")
    c4.metric("Win Rate", f"{win_rate:.1f}%", f"{len(wins)}/{total_trades}")
    c5.metric("Profit Factor", f"{profit_factor:.2f}")

    # ───── Unmatched Data ─────────────────────────────────────────────────────────────
    st.subheader("Unmatched Data")
    st.markdown(f"- Signals: **{len(unmatched_signals)}**")
    st.markdown(f"- Fills:   **{len(unmatched_fills)}**")

    # ───── Equity Curve ───────────────────────────────────────────────────────────────
    st.subheader("Equity Curve")
    eq_curve = curve
    fig_eq = plot_equity_curve(eq_curve, title="Equity Curve")
    st.pyplot(fig_eq)

    # ───── Equity & Drawdown ──────────────────────────────────────────────────────────
    st.subheader("Equity & Drawdown")
    fig_ed = plot_equity_and_drawdown(eq_curve, title="Equity & Drawdown")
    st.pyplot(fig_ed)

    # ───── Slippage Histogram ─────────────────────────────────────────────────────────
    st.subheader("Slippage Histogram")
    slippages = [r.net_pnl for r in pnl_records]
    fig_slip = plot_slippage_histogram(slippages, title="Slippage Distribution")
    st.pyplot(fig_slip)

else:
    st.info(
        "Please upload both a TradingView alerts CSV and a Tradovate fills CSV to get started."
    )
