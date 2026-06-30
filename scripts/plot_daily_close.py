from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot daily close price from a normalized AKShare CSV.")
    parser.add_argument("csv_path", help="Input CSV with trade_date, symbol, and close columns.")
    parser.add_argument("output_path", help="Output image path, for example chapters/.../assets/601138_SH_daily_close.svg.")
    parser.add_argument("--title", default=None, help="Optional chart title.")
    return parser.parse_args()


def load_daily_close(csv_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(csv_path, parse_dates=["trade_date"])
    required_columns = {"symbol", "trade_date", "close"}
    missing = sorted(required_columns.difference(frame.columns))
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    frame = frame[["symbol", "trade_date", "close"]].copy()
    frame["close"] = pd.to_numeric(frame["close"], errors="raise")
    return frame.sort_values("trade_date").reset_index(drop=True)


def plot_daily_close(frame: pd.DataFrame, csv_path: Path, output_path: Path, title: str | None) -> None:
    symbol = str(frame["symbol"].iloc[0])
    first_date = frame["trade_date"].iloc[0].date()
    last_date = frame["trade_date"].iloc[-1].date()

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 6.2))

    ax.plot(frame["trade_date"], frame["close"], color="#126f83", linewidth=2.4)
    ax.scatter(frame["trade_date"].iloc[-1], frame["close"].iloc[-1], color="#f05a28", s=42, zorder=3)

    ax.set_title(title or f"{symbol} Daily Close Price", fontsize=17, fontweight="bold", pad=16)
    ax.set_xlabel("Trade date")
    ax.set_ylabel("Close price")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.text(
        0,
        -0.18,
        f"{first_date} to {last_date} | {len(frame)} trading days | Source file: {csv_path.as_posix()}",
        transform=ax.transAxes,
        color="#65758b",
        fontsize=9,
    )

    fig.autofmt_xdate(rotation=0)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, format=output_path.suffix.lstrip(".") or "svg")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv_path)
    output_path = Path(args.output_path)
    frame = load_daily_close(csv_path)
    plot_daily_close(frame, csv_path, output_path, args.title)
    print(output_path)
    print(f"rows={len(frame)}")
    print(f"symbol={frame['symbol'].iloc[0]}")
    print(f"first_trade_date={frame['trade_date'].iloc[0].date()}")
    print(f"last_trade_date={frame['trade_date'].iloc[-1].date()}")


if __name__ == "__main__":
    main()
