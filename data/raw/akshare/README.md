# AKShare Raw Daily Data

这里保存通过 AKShare 公开接口获取的 A 股日线数据。

## Current File

- `000001_SZ_daily_20250629_20260629.csv`
- 股票：`000001.SZ`
- 数据源：`akshare.stock_zh_a_hist`
- 区间：`2025-06-29` 至 `2026-06-29`
- 实际交易日：`2025-06-30` 至 `2026-06-29`
- 行数：`242`

## Reproduce

```powershell
python scripts/fetch_akshare_daily.py --symbol 000001
```

## Columns

- `source`: 数据接口
- `symbol`: 股票代码
- `trade_date`: 交易日
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量
- `amount`: 成交额
- `amplitude`: 振幅
- `pct_chg`: 涨跌幅
- `change`: 涨跌额
- `turnover_rate`: 换手率
