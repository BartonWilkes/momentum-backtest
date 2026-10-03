import yfinance as yf
import os
import pandas as pd

tickers = ["BAC", "C", "GE", "MSFT", "F", "T", "AIG", "LEN", "AA", "LUV", "HD", "NEM"]

os.makedirs("data", exist_ok=True)

for ticker in tickers:
    print(f"Downloading {ticker}...")
    df = yf.download(ticker, start="2005-01-01", end="2015-01-01", auto_adjust=True)

    #flatten multi-level columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    print(f"  Shape: {df.shape}")
    print(f"  Missing values:\n{df.isna().sum()}")

    df = df.ffill()

    df.to_csv(f"data/{ticker}.csv")
    print(f"  Saved to data/{ticker}.csv\n")
