from pathlib import Path

import pytest

from quant_data_engine import CsvPriceSource, DataEngine


SAMPLE_CSV = Path(__file__).parents[1] / "chapters" / "01-data-engine" / "sample_prices.csv"


def test_loads_symbols_from_csv_source() -> None:
    engine = DataEngine.from_source(CsvPriceSource(SAMPLE_CSV))

    assert engine.symbols() == ["AAPL", "MSFT"]


def test_filters_history_by_symbol_and_dates() -> None:
    engine = DataEngine.from_source(CsvPriceSource(SAMPLE_CSV))

    history = engine.history("aapl", start="2024-01-03", end="2024-01-04")

    assert history["symbol"].tolist() == ["AAPL", "AAPL"]
    assert history["close"].tolist() == [184.25, 181.91]


def test_latest_raises_for_unknown_symbol() -> None:
    engine = DataEngine.from_source(CsvPriceSource(SAMPLE_CSV))

    with pytest.raises(LookupError):
        engine.latest("TSLA")

