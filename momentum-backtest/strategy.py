#Using moving average crossover strategy: uses 1 short term moving average (eg. 20 days) and 1 long term (eg. 50 days). When short term average>long term average,
#signals upward momentum, so buy. and vice versa.

import pandas as pd

def generate_signals(csv_path, short_window=20, long_window=50):
    # load the CSV saved
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)

    # calculate the two moving averages based on the Close price
    df["SMA_short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_long"] = df["Close"].rolling(window=long_window).mean()

    # create a "signal" column: 1 means "be invested", 0 means "stay out"
    df["signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "signal"] = 1

    # "position" shows when the signal actually changes (i.e. when we'd trade)
    df["position"] = df["signal"].diff()

    return df

if __name__ == "__main__":
    df = generate_signals("data/AAPL.csv")
    print(df[["Close", "SMA_short", "SMA_long", "signal", "position"]].tail(20))

    trades = df[df["position"] != 0]
    print(trades[["Close", "SMA_short", "SMA_long", "position"]])