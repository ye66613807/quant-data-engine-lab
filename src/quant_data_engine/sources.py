from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]


class CsvPriceSource:
    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)

    def load(self) -> pd.DataFrame:
        frame = pd.read_csv(self.csv_path, parse_dates=["timestamp"])
        missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

        frame = frame[REQUIRED_COLUMNS].copy()
        frame["symbol"] = frame["symbol"].astype(str).str.upper()
        frame = frame.sort_values(["symbol", "timestamp"]).reset_index(drop=True)
        return frame

