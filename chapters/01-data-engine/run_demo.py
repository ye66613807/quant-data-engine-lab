from pathlib import Path

from quant_data_engine import CsvPriceSource, DataEngine


def main() -> None:
    csv_path = Path(__file__).with_name("sample_prices.csv")
    source = CsvPriceSource(csv_path)
    engine = DataEngine.from_source(source)

    print("Symbols:", ", ".join(engine.symbols()))
    print()
    print("AAPL history:")
    print(engine.history("AAPL"))
    print()
    print("Latest MSFT bar:")
    print(engine.latest("MSFT"))


if __name__ == "__main__":
    main()

