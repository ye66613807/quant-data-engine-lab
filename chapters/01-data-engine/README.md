# Chapter 01: 从零搭建数据引擎

本章实现一个最小可用的数据引擎。它不依赖真实券商 API，先用 CSV 行情文件模拟数据源，把重点放在结构设计上。

## 核心概念

- **Source**: 数据从哪里来，例如 CSV、数据库、交易所 API。
- **Model**: 数据进入系统后的统一形态，例如 OHLCV K 线。
- **Engine**: 对外提供稳定查询接口，隐藏底层数据源差异。
- **Cache**: 将慢数据保存到本地，减少重复读取和请求。

## 当前实现

```python
from quant_data_engine import CsvPriceSource, DataEngine

source = CsvPriceSource("sample_prices.csv")
engine = DataEngine.from_source(source)

print(engine.symbols())
print(engine.history("AAPL"))
print(engine.latest("MSFT"))
```

## 下一步

- 增加真实数据源适配器
- 增加交易日历
- 增加复权处理
- 增加分钟线/日线频率转换
- 为第 2 章回测引擎提供稳定接口

