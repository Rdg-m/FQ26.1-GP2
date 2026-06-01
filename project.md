# Back-da-dev Project Reference

## 1. Overview

`Back-da-dev` is a Python library for rapid quantitative backtesting and strategy prototyping. The project was developed as a student lab for the FEA.dev community and is intended to help learners and curious investors:

- load historical market data,
- clean and normalize time-series data,
- execute trading strategy simulations,
- generate results and simple reports,
- explore strategy behavior with built-in models.

This repository is structured as a library package, with a public interface module at `src/back_da_dev` and implementation details split across `backtesting`, `dataprocessing`, `graphing`, and `interface` modules.

## 2. Current Status

The project currently includes:

- a public package entrypoint under `src/back_da_dev/__init__.py`
- a backtesting execution engine in `src/backtesting/backtesting_main.py`
- built-in strategy models in `src/backtesting/modelos_pre_implementados.py`
- data loading from local files and `yfinance` in `src/dataprocessing/load.py`
- data cleaning and validation in `src/dataprocessing/clean.py`
- graph generation helpers in `src/graphing/graphing.py`
- a high-level interface hub in `src/interface/interface.py`
- a minimal CLI entrypoint in `src/back_da_dev/__main__.py`

The repository is installable via `python -m pip install -e .` and targets Python `>=3.11`.

## 3. Packaging and Metadata

### Package name

- PyPI-style package name: `Back_da_dev`

### Project metadata

- `name = "Back_da_dev"`
- `version = "0.0.1"`
- `requires-python = ">=3.11"`
- dependencies:
  - `matplotlib`
  - `numpy`
  - `pandas`
  - `requests`
  - `yfinance`

### Package layout

- package source root: `src`
- package discovery: `src` directory
- package entrypoints: `back_da_dev`, `backtesting`, `dataprocessing`, `graphing`, `interface`

## 4. Repository Structure

### Top-level files

- `README.md` — concise project summary and usage examples
- `pyproject.toml` — packaging metadata and dependencies
- `requirements.txt` — dependency list for development/installation
- `fluxogram.md` — architecture notes and implementation roadmap
- `tests/` — unit tests for engine, strategies, interface and packaging

### Source packages

- `src/back_da_dev/` — public package exports
- `src/backtesting/` — engine and strategy models
- `src/dataprocessing/` — data loading and cleaning utilities
- `src/graphing/` — plotting utilities
- `src/interface/` — high-level orchestration hub

### Data

- `data/` — historical data files for B3 and S&P 500 examples
- `data/historical_data/B3/` — raw text series from B3
- `data/historical_data/S&P500/` — sample CSV files

## 5. Public API

The public API exported by `back_da_dev` includes:

- `BacktestEngine`
- `BacktestResult`
- `load_data`
- `clean_data`
- `load_and_clean`
- `resolve_strategy`
- `run_standard_backtest`
- `generate_backtest_report`
- `save_backtest_log`
- `export_backtest_graphs`
- `list_strategies`
- `main`

### Example import

```python
from back_da_dev import (
    BacktestEngine,
    load_and_clean,
    load_data,
    clean_data,
    resolve_strategy,
    run_standard_backtest,
    generate_backtest_report,
    list_strategies,
)
```

## 6. High-Level Workflow

The intended execution flow is:

1. load historical data via `load_data()` or `load_and_clean()`.
2. clean the raw data via `clean_data()`.
3. build a backtest engine with `BacktestEngine(...)`.
4. resolve a trading strategy with `resolve_strategy(...)`.
5. execute the strategy with `engine.run(strategy_instance)`.
6. compute metrics and persist reports with `generate_backtest_report(...)`.

The `interface` module exposes this flow through functions such as `run_standard_backtest()` and `generate_backtest_report()`.

## 7. Data Loading

### `src/dataprocessing/load.py`

`load_data()` supports two main modes:

- local file loading using `caminho` and `formato`
- API loading from `yfinance` using `indice`, `fonte`, `tempo`, `comeco`, and `fim`

Supported local formats:

- `csv`
- `json`
- `xlsx`

Supported data source names:

- `yfinance` (default)
- `bcb` (optional, requires the `bcb` dependency installed separately)

### Expected columns

The loader validates that the returned DataFrame contains:

- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

If any of those columns are missing, `load_data()` raises `KeyError`.

### Example

```python
from dataprocessing.load import load_data

raw_df = load_data(indice='PETR4.SA', fonte='yfinance', tempo='5y')
```

## 8. Data Cleaning

### `src/dataprocessing/clean.py`

`clean_data()` performs the following operations:

- converts the index to `datetime` if needed
- casts OHLC columns to numeric values
- fills missing `Volume` values with zero
- removes index duplicates
- sorts by index
- imputes or drops missing values using `ffill`, `bfill`, `interpolate`, or `drop`
- removes inconsistent rows where `High < Low` or negative prices are present
- optionally removes outliers using a z-score filter on `Close` returns

### Example

```python
from dataprocessing.clean import clean_data

clean_df = clean_data(raw_df, handle_missing='ffill', remove_outliers=True)
```

## 9. Strategies

### Base strategy class: `estrat`

Defined in `src/backtesting/modelos_pre_implementados.py`, `estrat` is the base class for all built-in strategies. It provides:

- memory storage for symbol prices
- a helper for generating standardized signals
- a `generate_signals(ohlcv)` method that adapts DataFrame or list inputs
- a required `com(assets)` method to be implemented by subclasses

### Built-in strategies

#### `buy_and_hold`

- buys each asset once on the first data point
- splits available capital equally among assets
- does not sell again

#### `MA`

- uses two simple moving averages
- buys when the fast SMA crosses above the slow SMA
- sells when the fast SMA crosses below the slow SMA
- stores the last decision for crossover detection

#### `EMA`

- inherits the MA strategy
- computes exponential moving averages instead of simple moving averages

### Strategy signal format

Strategies return signals in the form:

```python
{
    'symbol': 'PETR4',
    'signal_type': 'BUY' or 'SELL',
    'price': 25.50,
    'quantity': 100,
    'reason': 'text description',
}
```

## 10. Backtest Engine

### `src/backtesting/backtesting_main.py`

`BacktestEngine` is the core execution engine.

#### Constructor

```python
BacktestEngine(data, symbols, initial_capital=10000.0, commission=0.001)
```

Key fields:

- `data`: historical OHLCV data
- `symbols`: list of symbols to simulate
- `initial_capital`: starting cash
- `commission`: per-trade commission factor
- `cash`: current available cash
- `portfolio_value`: current cash plus open position value
- `_configs`: engine configuration dictionary
- `open_positions`: currently held positions
- `closed_positions`: list of closed trades
- `daily_history`: daily portfolio snapshots

#### Execution modes

The engine supports two modes controlled by `_configs['dado_real']`:

- real data mode (`True`) — iterates over the provided `data` index and runs `_run_normal()`
- synthetic Brownian mode (`False`) — generates synthetic OHLCV with `_run_brown()`

#### Normal mode

`_run_normal()` processes the loaded data by unique dates. For each date it:

- slices `ohlcv` for that date
- calls `_fluxo_padrao(ohlcv, strategy_instance)`

#### Brownian mode

`_run_brown()` generates synthetic price series using `MBG` from `src/dataprocessing/mov_brow.py` and then runs the normal strategy flow on the generated OHLCV.

#### Signal processing

`_fluxo_padrao()`:

- asks the strategy for signals with `generate_signals(ohlcv)`
- executes buy/sell signals with `_execute_buy()` and `_execute_sell()`
- checks stop-loss and take-profit rules with `_verificar_stop_take()`
- updates portfolio value and appends `daily_history`

#### Buying logic

`_execute_buy()`:

- calculates total cost including commission
- rejects impossible buys unless `_configs['over_spend'] == True`
- supports aggregation of buys into existing open positions
- updates `cash` and `open_positions`

#### Selling logic

`_execute_sell()`:

- sells up to the requested quantity
- updates cash after commission
- records closed trades in `closed_positions`
- decrements open position quantity and deletes it when fully closed

### Portfolio and history

The engine stores daily snapshots in `daily_history` with:

- `date`
- `cash`
- `portfolio_value`

This history is used by the interface to compute drawdown and generate graphs.

## 11. Interface Hub

### `src/interface/interface.py`

This module provides the high-level orchestration functions used by the library API and CLI.

Key responsibilities:

- resolve strategy names to strategy instances
- combine data loading and cleaning in `load_and_clean()`
- build a configured engine in `build_backtest_engine()`
- compute summary metrics in `compute_backtest_metrics()`
- save log files and graphs
- expose `run_standard_backtest()` for a turnkey workflow

### `run_standard_backtest()`

This function performs:

1. optional loading and cleaning of data
2. engine construction
3. strategy resolution
4. engine execution
5. metrics computation
6. graph and log export

### Metrics available

The interface computes:

- initial capital
- final cash
- final equity
- net return
- return percentage
- number of trades closed
- win rate
- total profit
- maximum drawdown percentage
- duration in days
- annualized return percentage

`compute_backtest_metrics()` derives drawdown and annualized return from `engine.daily_history`.

## 12. Graphing

### `src/graphing/graphing.py`

Graph utilities include:

- `plot_time_series()` — general price/time plotting
- `plot_equity_curve()` — portfolio equity over time
- `plot_drawdown()` — drawdown visualization

The module also exposes technical indicator helpers:

- `calculate_rsi()`
- `calculate_macd()`
- `calculate_bollinger_bands()`
- `calculate_discrete_yields()`
- `discrete_to_continuous()`

Graphs are styled through a theme helper and use Matplotlib.

### Graph export

`export_backtest_graphs()` in the interface saves:

- `backtest_equity_curve.png`
- `backtest_drawdown.png`

These files are written to the selected output directory.

## 13. CLI Usage

The executable CLI entrypoint is `src/back_da_dev/__main__.py`, which simply calls `main()` from `src/interface/interface.py`.

### Example

```bash
python -m back_da_dev --indice PETR4.SA --strategy ma --initial-capital 10000 --output-dir ./results
```

### CLI options

- `--indice` — ticker to load via `yfinance`
- `--symbols` — explicit symbols list for the backtest
- `--strategy` — `buy_and_hold`, `ma`, or `ema`
- `--initial-capital` — starting cash
- `--commission` — commission rate
- `--output-dir` — output path for graphs/logs
- `--no-graphs` — disable graph export
- `--no-log` — disable log export
- `--tempo` — yfinance period
- `--fonte` — data source name
- `--caminho` — local file path
- `--formato` — local file format

## 14. Example End-to-End Backtest

```python
from back_da_dev import load_and_clean, run_standard_backtest, list_strategies

raw_df = load_and_clean(indice='PETR4.SA', fonte='yfinance', tempo='5y')

result = run_standard_backtest(
    data=raw_df,
    strategy='buy_and_hold',
    initial_capital=10000.0,
    commission=0.001,
    save_graphs=True,
    save_log=True,
    output_dir='./results',
)

print(result.metrics)
print(result.graph_paths)
print(result.log_path)
```

## 15. Limitations and Known Gaps

This project is a working prototype and currently has some limitations:

- engine metrics are computed in the interface layer, not inside `BacktestEngine`
- the backtest engine currently supports only simple stop-loss/take-profit logic and no risk position sizing beyond quantity calculation
- data loading is limited to `csv`, `json`, `xlsx`, `yfinance`, and optional `bcb`
- synthetic Brownian mode is available, but only in the engine's fictitious simulation path
- graph export is limited to equity curve and drawdown charts
- `clean_data()` does not return an explicit report object, only a cleaned DataFrame
- `load_and_clean()` forces `symbol` column injection only when `indice` is provided

## 16. Roadmap and Future Improvements

Potential next steps for the project include:

- add richer metrics inside `BacktestEngine` (Sharpe, Sortino, profit factor)
- improve multi-asset support and full portfolio allocation rules
- add instrument-level trade logging and CSV/JSON exports
- expand graphing to trade overlays and distribution charts
- add more strategy templates and an extensible strategy registry
- add stronger validation and error handling in `load_data()` and `clean_data()`
- document the package API with generated reference docs

## 17. Tests

Run the test suite with:

```bash
pytest -q
```

The repository includes tests for:

- engine behavior
- strategy generation
- package imports
- interface workflows
- packaging sanity

## 18. Reference Notes

- `src/back_da_dev/__init__.py` defines the package public API
- `src/interface/interface.py` is the recommended integration layer for library users
- `src/backtesting/modelos_pre_implementados.py` defines strategies and signal semantics
- `src/backtesting/backtesting_main.py` contains engine state and execution loops
- `src/dataprocessing/load.py` and `src/dataprocessing/clean.py` manage input data
- `src/graphing/graphing.py` provides visual output helpers

---

This document is intended as a deep reference for developers working on `Back-da-dev` and should be updated as the project evolves.