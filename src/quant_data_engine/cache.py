from pathlib import Path

import pandas as pd


class ParquetCache:
    def __init__(self, cache_dir: str | Path) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, name: str) -> Path:
        return self.cache_dir / f"{name}.parquet"

    def exists(self, name: str) -> bool:
        return self.path_for(name).exists()

    def read(self, name: str) -> pd.DataFrame:
        return pd.read_parquet(self.path_for(name))

    def write(self, name: str, frame: pd.DataFrame) -> Path:
        path = self.path_for(name)
        frame.to_parquet(path, index=False)
        return path

