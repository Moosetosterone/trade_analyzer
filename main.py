# main.py
from data.importer import TradingViewCSVImporter, TradovateCSVImporter


def main():
    tv_importer = TradingViewCSVImporter()
    tradovate_importer = TradovateCSVImporter()

    signals_df = tv_importer.import_data(
        "data/TradingView_Alerts_Log_2025-07-03_790cd.csv"
    )
    fills_df = tradovate_importer.import_data(
        fill_source="data/Orders-4.csv", cash_source="data/Cash History.csv"
    )

    print("TradingView Signals:")
    print(signals_df.head())
    print("\nTradovate Fills with Commissions:")
    print(fills_df.head())


if __name__ == "__main__":
    main()
