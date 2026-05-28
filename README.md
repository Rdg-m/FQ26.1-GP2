# FQ26.1-GP2

## Project Title & Tagline
**FEA.dev Backtesting Lab** — Fast prototyping and quantitative strategy backtesting for student researchers and curious investors.

## Table of Contents
- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Python API](#python-api)
  - [CLI](#cli)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## About the Project
This repository is a compact FEA.dev student project for fast backtesting and quantitative strategy prototyping. The code is designed to help league members explore trading ideas, validate signals, and generate performance summaries using historical market data.

It combines data ingestion, cleanup, strategy execution, and result visualization into a simple workflow. The goal is to make early quant research easy to iterate on while staying close to real-market concepts like commission, drawdown, and trade outcomes.

## Built With
- Python `>=3.11`
- `pandas` for time series and data pipeline handling
- `numpy` for numeric operations
- `matplotlib` for result visualization
- `requests` for API access
- `yfinance` for market history download
- `pytest` for test coverage

## Getting Started

### Prerequisites
- Python `3.11` or newer
- `pip` package manager
- Optionally, a virtual environment tool: `venv`, `virtualenv`, or `pipenv`

### Installation
From the repository root:

```bash
python -m pip install -e .
```

If you prefer a dedicated environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.\.venv\Scripts\activate  # Windows
python -m pip install -e .
```

### Configuration
This project does not require special environment variables by default.

- Use `yfinance` as the default data source
- Place local files in `./data/` when loading from disk
- If you need additional data providers, install optional dependencies manually

> If your workflow uses an external API or private credentials, add those details here later.

## Usage

### Python API
Import the public package entry point:

```python
from back_da_dev import run_standard_backtest, load_and_clean, list_strategies

raw_df = load_and_clean(indice="PETR4.SA", fonte="yfinance", tempo="5y")

result = run_standard_backtest(
    data=raw_df,
    strategy="buy_and_hold",
    initial_capital=10000.0,
    commission=0.001,
    save_graphs=False,
    save_log=False,
)

print(result.metrics)
```

Generate a report after a backtest:

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

### CLI
Run the package as a module:

```bash
python -m back_da_dev --indice PETR4.SA --strategy ma --initial-capital 10000 --output-dir ./results
```

Example options:
- `--indice`: ticker symbol for yfinance load
- `--strategy`: `buy_and_hold`, `ma`, or `ema`
- `--initial-capital`: starting capital
- `--commission`: trading commission rate
- `--output-dir`: where graphs and logs are saved
- `--no-graphs`: disable graph generation
- `--no-log`: disable log output

## API Documentation
The public package exposes the main backtesting workflow:

- `BacktestEngine` — core engine for running strategy simulations
- `load_data(...)` — load historical data from local files or `yfinance`
- `clean_data(...)` — clean, normalize, and validate loaded data
- `load_and_clean(...)` — combined data load + cleanup flow
- `resolve_strategy(...)` — instantiate a built-in strategy by name
- `run_standard_backtest(...)` — execute a backtest and return metrics
- `generate_backtest_report(...)` — save graphs and logs for a completed run
- `save_backtest_log(...)` — serialize metrics and trade history to `.log`
- `list_strategies()` — list available strategy names

## Testing
Run the repository test suite with:

```bash
pytest -q
```

This project includes tests for:
- backtest engine behavior
- strategy signal generation
- package imports
- interface workflows
- packaging sanity

## Contributing
FEA.dev members and outside contributors are welcome.

- Fork the repository
- Create a descriptive branch
- Open a pull request with your feature or fix
- Include tests and update docs when needed
- Report bugs via issues if behavior differs from expected output

## License
This project is licensed under the MIT License.

See [LICENSE](./LICENSE) for details.

