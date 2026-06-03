# Back-da-dev Project Reference

## 1. Overview

Back-da-dev is a student-driven Python library for rapid financial backtesting and prototype strategy research. It combines data ingestion, cleaning, strategy execution, reporting, and plotting into a small experimental package intended for academic exploration and quick iteration.

The repository is organized as a package with the top-level package name `Back_da_dev` and a source layout under `src/`. It is meant to be used both as a library and as a CLI module.

### 1.1 Goals

- Provide a simple, reusable workflow for financial backtesting
- Support loading historical prices from local files and `yfinance`
- Allow plug-in strategy objects that generate buy/sell signals
- Simulate execution with commission and portfolio tracking
- Export graphs and textual logs for backtest results
- Document the project with a deep architecture reference

### 1.2 Current status

- Core backtesting engine implemented in `src/backtesting/backtesting_main.py`
- Data loading in `src/dataprocessing/load.py`
- Data cleaning in `src/dataprocessing/clean.py`
- Strategy prototypes in `src/backtesting/modelos_pre_implementados.py`
- Strategy utility functions in `src/backtesting/estrategy.py`
- Graphing utilities in `src/graphing/graphing.py`
- Public integration hub in `src/interface/interface.py`
- Package entrypoint in `src/back_da_dev/__init__.py`

## 2. Package Metadata

The project package is configured in `pyproject.toml` with:

- name: `Back_da_dev`
- version: `0.0.1`
- Python requirement: `>=3.11`
- Dependencies:
  - `matplotlib`
  - `numpy`
  - `pandas`
  - `requests`
  - `yfinance`
- Source layout: `src/`

### 2.1 Installation

```bash
python -m pip install -e .
```

For an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## 3. Architecture and Package Layout

The package is structured into the following logical layers:

- `src/back_da_dev/`: public package exports and CLI entrypoint
- `src/interface/`: high-level integration hub that wires load/clean/backtest/report
- `src/backtesting/`: backtest engine, built-in strategies, and strategy helpers
- `src/dataprocessing/`: data loading and cleaning utilities
- `src/graphing/`: plotting and visualization helpers

### 3.1 Root package exports

`src/back_da_dev/__init__.py` exports the public API:

- `BacktestEngine`
- `BacktestResult`
- `export_backtest_graphs`
- `generate_backtest_report`
- `list_strategies`
- `load_and_clean`
- `load_data`
- `main`
- `resolve_strategy`
- `run_standard_backtest`
- `save_backtest_log`
- `clean_data`

This file intentionally exposes the main workflow functions so users can import from `back_da_dev` after installation.

## 4. Data Pipeline

The library handles data in three stages:

1. Load raw historical data (`load_data`)
2. Clean and normalize it (`clean_data`)
3. Execute a backtest on the prepared data

### 4.1 Data loading

Implemented in `src/dataprocessing/load.py`.

Supported sources:

- Local files: `csv`, `json`, `xlsx`
- `yfinance` using an index/symbol and time range
- Banco Central do Brasil via optional `bcb` package when `fonte='bcb'`

Expected columns after load:

- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

The loader also supports saving downloaded data to a local `dados/` directory when `salvar=True`.

### 4.2 Data cleaning

Implemented in `src/dataprocessing/clean.py`.

The cleaning function:

- converts the index to `datetime`
- coerces OHLC columns to numeric values
- fills missing values using `ffill`, `bfill`, `interpolate`, or drops them
- removes duplicate timestamps
- sorts data by index
- drops obvious inconsistencies such as `High < Low` or negative prices
- optionally removes outliers from percentage returns using a z-score threshold

Function signature:

```python
clean_data(df, handle_missing='ffill', remove_outliers=False, verbose=True)
```

The current implementation returns a tuple `(df_limpo, df_report)` containing the cleaned DataFrame and a report DataFrame summarizing the cleaning operation.

## 5. Backtesting Engine

The main engine is in `src/backtesting/backtesting_main.py`.

### 5.1 BacktestEngine responsibilities

`BacktestEngine` manages:

- input historical data
- portfolio state and cash
- commission costs
- open and closed positions
- daily portfolio history
- execution logic for buy and sell signals
- support for two modes:
  - real historical data mode (`dado_real=True`)
  - geometric Brownian motion simulation mode (`dado_real=False`)

### 5.2 Engine internals

Key engine attributes:

- `data`: input DataFrame
- `symbols`: list of symbols under test
- `commission`: trading commission rate
- `initial_capital`: starting cash
- `cash`: available cash during simulation
- `portfolio_value`: current total value of cash plus open positions
- `_configs`: engine configuration map
- `open_positions`: open position dictionary
- `closed_positions`: list of closed trade dictionaries
- `daily_history`: list of daily portfolio snapshots

### 5.3 Execution flow

`BacktestEngine.run(strategy_instance)` chooses one of two routines:

- `_run_normal(strategy_instance)` when `_configs['dado_real']` is `True`
- `_run_brown(strategy_instance)` when `_configs['dado_real']` is `False`

Both flows use `_fluxo_padrao(ohlcv, strategy_instance)` to:

- generate signals from the strategy
- process each signal with `_processar_sinal`
- apply forced sales via `_verificar_stop_take`
- update portfolio value with `_atualizar_valor_protifolio`

### 5.4 Signal execution

The strategy interface expects signals in this structure:

```python
{
    'symbol': str,
    'signal_type': 'BUY' | 'SELL',
    'price': float,
    'quantity': int,
    'reason': str,
}
```

The engine handles buys and sells with `_execute_buy` and `_execute_sell`, taking commission into account.

### 5.5 Brownian mode

When `dado_real` is `False`, the engine generates synthetic prices by calling `MBG` from `src/dataprocessing/mov_brow.py` and then builds OHLCV-like rows for each period.

## 6. Strategies and Signals

Strategy prototypes are defined in `src/backtesting/modelos_pre_implementados.py` and utility functions are in `src/backtesting/estrategy.py`.

### 6.1 Strategy prototypes

Built-in strategy classes:

- `buy_and_hold`
- `MA`
- `EMA`

All strategies derive from the base class `estrat`, which provides:

- `generate_signals(ohlcv)` adapter
- `_generate_signal(...)` helper
- memory storage for historic prices

The base class also defines the abstract method `com(assets)` for signal generation.

### 6.2 Strategy behavior

- `buy_and_hold` buys all assets once and then holds them.
- `MA` generates long/short signals based on fast/slow moving average crossover with simple moving averages.
- `EMA` inherits `MA` and calculates exponential moving averages instead of simple moving averages.

### 6.3 Strategy utilities

`src/backtesting/estrategy.py` contains indicator functions and helper calculations such as:

- `adx`
- `sma`
- `ema`
- `macd`
- `rsi`
- `stochastic`
- `roc`
- `momentum`
- `bollinger_bands`
- `atr`
- `obv`
- `volume_roc`
- `mfi`

### 6.4 Public strategy alias

A user-friendly alias module was added at `src/backtesting/strategy.py` that re-exports the most important utilities from `estrategy.py`.

## 7. Integration Hub

The high-level interface is implemented in `src/interface/interface.py`.

### 7.1 Public workflow functions

- `list_strategies()` — list available built-in strategies
- `resolve_strategy(strategy, initial_capital, **strategy_kwargs)` — create a strategy instance from a name, class, or instance
- `load_and_clean(...)` — load data and then clean it
- `build_backtest_engine(...)` — instantiate `BacktestEngine` and apply configuration
- `compute_backtest_metrics(engine)` — compute return, drawdown, trade counts, and annualized return
- `save_backtest_log(engine, metrics, path)` — write a `.log` summary file
- `export_backtest_graphs(engine, output_dir, prefix)` — save equity and drawdown PNGs
- `generate_backtest_report(engine, output_dir, prefix, save_graphs, save_log)` — produce a full report
- `run_standard_backtest(...)` — full end-to-end backtest workflow

### 7.2 Backtest result object

`BacktestResult` contains:

- `engine`: the running `BacktestEngine`
- `metrics`: computed performance metrics
- `graph_paths`: saved chart paths
- `log_path`: optional saved log path

### 7.3 Metrics computed today

The interface currently computes:

- `initial_capital`
- `final_cash`
- `final_equity`
- `net_return`
- `total_trades`
- `return_pct`
- `winning_trades`
- `losing_trades`
- `win_rate`
- `total_profit`
- `max_drawdown_pct`
- `duration_days`
- `annualized_return_pct`

## 8. Graphing and Reporting

`src/graphing/graphing.py` provides plotting utilities and chart style helpers.

Key features:

- theming support (`dark`, `light`, `seaborn`)
- styled plot decorators
- technical indicator functions for RSI, MACD, Bollinger Bands
- `plot_time_series`
- `plot_equity_curve`
- `plot_drawdown`

Supported charts (available via the interface/export):

- `equity_curve` — Curva de patrimônio (valor total do portfolio ao longo do tempo)
- `drawdown` — Quedas relativas ao pico (drawdown %)
- `cumulative_returns` — Retorno acumulado (%) ao longo do tempo
- `volatility` — Volatilidade móvel anualizada (rolling window)
- `bollinger` — Preço com Bandas de Bollinger (média + bandas)
- `rsi` — Índice de Força Relativa (RSI)
- `time_series` — Série temporal de preço (plot_time_series)

Behavior / integration notes:

- The `interface` exposes `export_backtest_graphs(..., charts=[...], formats=[...])` which can generate any of the supported charts and save them to disk.
- By default the CLI and API generate `equity_curve` and `drawdown`. You may request additional charts via the `charts` parameter or the CLI flag `--charts`.
- When a chart requires price series input (ex: `bollinger`, `rsi`, `cumulative_returns`, `volatility`) the interface will attempt to construct a `price_series` from the engine `daily_history` using one of the columns `close`, `price` or `portfolio_value`.
- If the required input is missing the interface skips that chart and emits a warning.

Example: generate a report with extra charts via Python API:

```python
from back_da_dev import generate_backtest_report

report = generate_backtest_report(
  engine=engine,
  output_dir='./results',
  prefix='experiment1',
  save_graphs=True,
  charts=['equity_curve','cumulative_returns','rsi','bollinger'],
  formats=('png','svg'),
)
print(report.graph_paths)
```

Example: CLI generation with specific charts and formats:

```bash
python -m back_da_dev --indice PETR4.SA --strategy ma --output-dir ./results --charts equity_curve rsi bollinger --chart-formats png svg
```

The interface uses these functions to export PNG charts for equity and drawdown.

## 9. CLI

The package supports a minimal CLI through `src/back_da_dev/__main__.py`, which delegates to `interface.main()`.

CLI options include:

- `--indice` — ticker symbol for `yfinance`
- `--symbols` — explicit symbol list for the backtest
- `--strategy` — built-in strategy name (`buy_and_hold`, `ma`, `ema`)
- `--initial-capital`
- `--commission`
- `--output-dir`
- `--no-graphs`
- `--no-log`
- `--tempo`
- `--fonte`
- `--caminho`
- `--formato`

The CLI is invoked by:

```bash
python -m back_da_dev --indice PETR4.SA --strategy ma --initial-capital 10000 --output-dir ./results
```

Use `python3 -m pip install -e .` to install the package and run the CLI, or run directly from source:

```bash
PYTHONPATH=src python3 -m back_da_dev --indice PETR4.SA --strategy ma --initial-capital 10000 --output-dir ./results
```

## 10. Usage Examples

### 10.1 Library example

```python
from back_da_dev import run_standard_backtest, load_and_clean, list_strategies

result = run_standard_backtest(
    strategy="buy_and_hold",
    initial_capital=10000.0,
    commission=0.001,
    load_kwargs={"indice": "PETR4.SA", "fonte": "yfinance", "tempo": "5y"},
    save_graphs=False,
    save_log=False,
)

print(result.metrics)
```

### 10.2 Report generation

```python
from back_da_dev import generate_backtest_report

report = generate_backtest_report(
    engine=result.engine,
    output_dir="./results",
    prefix="feadev_backtest",
)
print(report.graph_paths)
print(report.log_path)
```

## 11. Tests

Run the test suite with:

```bash
pytest -q
```

Current tests cover:

- import and package loading
- backtest engine behavior
- strategy execution
- interface flow
- packaging sanity

## 12. Known limitations

The project is a prototype and currently has several limitations:

- The interface workflow assumes `clean_data()` returns a DataFrame, but the implementation currently returns `(df_limpo, df_report)`.
- Strategy coverage is limited to a small set of built-in prototypes.
- `BacktestEngine` metrics do not yet include Sharpe, Sortino, or profit factor.
- The CLI is minimal and does not expose all internal configuration options.
- Data validation is basic; advanced handling of splits, dividends, and multi-asset data is not yet implemented.
- Graphing exports are limited to equity and drawdown charts.

## 13. Roadmap

Recommended next improvements:

- complete the integration flow between loader, cleaner, engine, and interface
- add full trade-level and portfolio-level metrics
- expand strategy library and plugin support
- add CSV/JSON export of results and trade history
- improve CLI coverage and output customization
- add tests for `load.py`, `clean.py`, `graphing.py`, and reporting output
- add documentation for package installation and contribution guidelines

## 14. Appendix: public API summary

### Public classes

- `back_da_dev.BacktestEngine`
- `back_da_dev.BacktestResult`

### Public functions

- `back_da_dev.list_strategies`
- `back_da_dev.resolve_strategy`
- `back_da_dev.load_and_clean`
- `back_da_dev.build_backtest_engine`
- `back_da_dev.compute_backtest_metrics`
- `back_da_dev.generate_backtest_report`
- `back_da_dev.export_backtest_graphs`
- `back_da_dev.save_backtest_log`
- `back_da_dev.run_standard_backtest`
- `back_da_dev.clean_data`
- `back_da_dev.load_data`
- `back_da_dev.main`
- `backtesting.estrategy`
