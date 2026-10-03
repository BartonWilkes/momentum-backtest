import pandas as pd
import matplotlib.pyplot as plt
from strategy import generate_signals

def run_backtest(csv_path):
    df = generate_signals(csv_path)

    # daily return of just holding the stock (buy-and-hold)
    df["daily_return"] = df["Close"].pct_change()

    # strategy return: only earn the day's return if we were invested (signal==1)
    # we use .shift(1) because we only know today's signal AFTER today's close,
    # so we can only act on it from tomorrow
    df["strategy_return"] = df["daily_return"] * df["signal"].shift(1)

    # cumulative growth of $1 invested, for both approaches
    df["cumulative_market"] = (1 + df["daily_return"]).cumprod()
    df["cumulative_strategy"] = (1 + df["strategy_return"]).cumprod()

    return df

if __name__ == "__main__":
    df = run_backtest("data/MSFT.csv")

    print(df[["cumulative_market", "cumulative_strategy"]].tail())

    # plot both so we can see them side by side
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["cumulative_market"], label="Buy & Hold")
    plt.plot(df.index, df["cumulative_strategy"], label="Strategy")
    plt.legend()
    plt.title("Strategy vs Buy & Hold: Growth of $1")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.savefig("results/equity_curve_MSFT-2005.png")
    plt.show()