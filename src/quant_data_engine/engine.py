from datetime import datetime

import pandas as pd


class DataEngine:
    def __init__(self, frame: pd.DataFrame) -> None:
        self.frame = frame.copy()

    @classmethod
    def from_source(cls, source: object) -> "DataEngine":
        if not hasattr(source, "load"):
            raise TypeError("source must provide a load() method")
        return cls(source.load())

    def symbols(self) -> list[str]:
        return sorted(self.frame["symbol"].unique().tolist())

    def history(
        self,
        symbol: str,
        start: str | datetime | None = None,
        end: str | datetime | None = None,
    ) -> pd.DataFrame:
        symbol = symbol.upper()
        result = self.frame[self.frame["symbol"] == symbol].copy()

        if start is not None:
            result = result[result["timestamp"] >= pd.Timestamp(start)]
        if end is not None:
            result = result[result["timestamp"] <= pd.Timestamp(end)]

        return result.reset_index(drop=True)

    def latest(self, symbol: str) -> pd.Series:
        history = self.history(symbol)
        if history.empty:
            raise LookupError(f"No bars found for symbol: {symbol.upper()}")
        return history.iloc[-1]

