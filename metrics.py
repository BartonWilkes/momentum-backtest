import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from backtest import run_backtest


def calculate_stats(df, freq=252):
    strat_returns = df["strategy_return"].dropna()
    market_returns = df["daily_return"].dropna()

    def stats_for(returns, invested_only=False):
        total_return = (1 + returns).prod() - 1
        cagr = (1 + returns).prod() ** (freq / len(returns)) - 1
        vol = returns.std() * np.sqrt(freq)
        sharpe = (returns.mean() * freq) / vol if vol != 0 else np.nan

        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_dd = drawdown.min()

        if invested_only:
            active_returns = returns[returns != 0]
            if len(active_returns) > 0:
                win_rate = len(active_returns[active_returns > 0]) / len(active_returns)
            else:
                win_rate = np.nan
        else:
            win_rate = (returns > 0).mean()

        return {
            "Total Return": total_return,
            "CAGR": cagr,
            "Volatility": vol,
            "Sharpe": sharpe,
            "Max Drawdown": max_dd,
            "Win Rate": win_rate
        }

    return {
        "Strategy": stats_for(strat_returns, invested_only=True),
        "Buy & Hold": stats_for(market_returns, invested_only=False)
    }


def plot_ticker(df, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["cumulative_market"], label="Buy & Hold")
    plt.plot(df.index, df["cumulative_strategy"], label="Strategy")
    plt.legend()
    plt.title(f"{ticker}: Strategy vs Buy & Hold (Growth of $1)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")

    # unique filename per ticker so nothing overwrites previous charts
    filename = f"results/metrics_curve_{ticker}.png"
    plt.savefig(filename)
    plt.close()  # closes the figure so it doesn't stay open in memory/pop up repeatedly
    print(f"  Saved chart to {filename}")


if __name__ == "__main__":
    tickers = ["BAC", "C", "GE", "MSFT", "F", "T", "AIG", "LEN", "AA", "LUV", "HD", "NEM"]
    all_results = {}

    for ticker in tickers:
        df = run_backtest(f"data/{ticker}.csv")
        stats = calculate_stats(df)
        all_results[ticker] = stats

        plot_ticker(df, ticker)

    for ticker, result in all_results.items():
        print(f"\n=== {ticker} ===")
        summary = pd.DataFrame(result).T
        print(summary.round(3))