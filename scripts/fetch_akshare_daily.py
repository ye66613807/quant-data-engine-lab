from __future__ import annotations

import argparse
import time
from datetime import date, timedelta
from pathlib import Path

import akshare as ak
import pandas as pd


COLUMN_MAP = {
    "日期": "trade_date",
    "股票代码": "symbol",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "pct_chg",
    "涨跌额": "change",
    "换手率": "turnover_rate",
}


def one_year_ago(today: date) -> date:
    try:
        return today.replace(year=today.year - 1)
    except ValueError:
        return today - timedelta(days=365)


def compact_date(value: date) -> str:
    return value.strftime("%Y%m%d")


def stock_suffix(symbol: str) -> str:
    return "SH" if symbol.startswith("6") else "SZ"


def normalize_daily_frame(frame: pd.DataFrame, symbol: str, source: str) -> pd.DataFrame:
    frame = frame.rename(columns=COLUMN_MAP).copy()
    frame["symbol"] = f"{symbol}.{stock_suffix(symbol)}"
    frame["source"] = source
    frame = frame[
        [
            "source",
            "symbol",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "amplitude",
            "pct_chg",
            "change",
            "turnover_rate",
        ]
    ]
    return frame.sort_values("trade_date").reset_index(drop=True)


def fetch_daily_frame(
    symbol: str,
    start_date: str,
    end_date: str,
    adjust: str,
    retries: int = 3,
) -> pd.DataFrame:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
            )
        except Exception as error:
            last_error = error
            if attempt == retries:
                break
            time.sleep(2 * attempt)

    raise RuntimeError(f"AKShare request failed after {retries} attempts") from last_error


def parse_args() -> argparse.Namespace:
    today = date.today()
    start = one_year_ago(today)

    parser = argparse.ArgumentParser(description="Fetch daily A-share data from AKShare.")
    parser.add_argument("--symbol", default="000001", help="A-share stock code, for example 000001.")
    parser.add_argument("--start-date", default=compact_date(start), help="Start date in YYYYMMDD.")
    parser.add_argument("--end-date", default=compact_date(today), help="End date in YYYYMMDD.")
    parser.add_argument("--adjust", default="", choices=["", "qfq", "hfq"], help="Adjustment mode.")
    parser.add_argument("--output-dir", default="data/raw/akshare", help="Directory for generated CSV files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    symbol = args.symbol.strip()
    frame = fetch_daily_frame(
        symbol=symbol,
        start_date=args.start_date,
        end_date=args.end_date,
        adjust=args.adjust,
    )
    if frame is None or frame.empty:
        raise SystemExit(f"No rows returned for {symbol} from {args.start_date} to {args.end_date}.")

    normalized = normalize_daily_frame(frame, symbol=symbol, source="akshare.stock_zh_a_hist")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{symbol}_{stock_suffix(symbol)}_daily_{args.start_date}_{args.end_date}.csv"
    output_path = output_dir / filename
    normalized.to_csv(output_path, index=False, encoding="utf-8")

    print(output_path)
    print(f"rows={len(normalized)}")
    print(f"first_trade_date={normalized['trade_date'].iloc[0]}")
    print(f"last_trade_date={normalized['trade_date'].iloc[-1]}")


if __name__ == "__main__":
    main()
