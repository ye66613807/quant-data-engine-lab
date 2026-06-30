# Quant Data Engine Lab

从零搭建量化交易数据引擎的学习仓库。

这个仓库采用“章节 + 可运行代码 + 对外展示页”的结构。第 1 章聚焦数据引擎的最小闭环：数据源、标准化、缓存、查询和后续策略研究的接口。

## Chapter 01: 从零搭建数据引擎

目标不是一次做一个庞大的交易系统，而是先建立一个可靠的数据底座：

- 统一行情数据结构
- 支持 CSV 数据源接入
- 支持本地缓存
- 提供简单的查询接口
- 为后续回测、因子研究、组合管理留出扩展位置

## Repository Layout

```text
quant-data-engine-lab/
├── chapters/
│   └── 01-data-engine/
│       ├── README.md
│       └── sample_prices.csv
├── docs/
│   └── index.html
├── data/
│   └── raw/
│       └── akshare/
│           ├── 000001_SZ_daily_20250629_20260629.csv
│           ├── 601138_daily_20250630_20260629.csv
│           └── README.md
├── src/
│   └── quant_data_engine/
│       ├── __init__.py
│       ├── cache.py
│       ├── engine.py
│       ├── models.py
│       └── sources.py
├── tests/
│   └── test_data_engine.py
├── .gitignore
└── pyproject.toml
```

## Quick Start

```powershell
cd quant-data-engine-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

运行一个最小示例：

```powershell
python chapters/01-data-engine/run_demo.py
```

## Raw Daily Data

`data/raw/akshare/` 保存通过 AKShare 获取或整理的 A 股日线 K 线数据：

- `000001_SZ_daily_20250629_20260629.csv`：平安银行，实际交易日 `2025-06-30` 至 `2026-06-29`，`242` 行
- `601138_daily_20250630_20260629.csv`：601138.SH，实际交易日 `2025-06-30` 至 `2026-06-02`，`242` 行

## Public Page

仓库包含 `docs/index.html`，可以通过 GitHub Pages 对外展示学习路线和章节入口。

建议仓库名：`quant-data-engine-lab`

建议 GitHub Pages 设置：

- Source: Deploy from a branch
- Branch: `main`
- Folder: `/docs`
