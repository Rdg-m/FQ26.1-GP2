import subprocess
import sys
from pathlib import Path

import pandas as pd

from back_da_dev import (
    run_standard_backtest,
    generate_backtest_report,
    list_strategies,
)


def _make_sample_data():
    dates = pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"])
    df = pd.DataFrame(
        {
            "symbol": ["A", "A", "A"],
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.5, 100.5, 101.5],
            "close": [101.0, 102.0, 103.0],
            "volume": [1000, 1200, 1100],
        },
        index=dates,
    )
    return df


def test_readme_api_run_and_list_strategies(tmp_path):
    df = _make_sample_data()

    result = run_standard_backtest(
        data=df,
        symbols=["A"],
        strategy="buy_and_hold",
        initial_capital=1000.0,
        commission=0.0,
        output_dir=tmp_path,
        save_graphs=False,
        save_log=False,
    )

    assert result is not None
    assert isinstance(result.metrics, dict)
    assert "final_equity" in result.metrics
    assert "buy_and_hold" in list_strategies()


def test_readme_generate_backtest_report_creates_files(tmp_path):
    df = _make_sample_data()

    result = run_standard_backtest(
        data=df,
        symbols=["A"],
        strategy="buy_and_hold",
        initial_capital=1000.0,
        commission=0.0,
        output_dir=tmp_path,
        save_graphs=False,
        save_log=False,
    )

    charts = ["equity_curve", "drawdown", "cumulative_returns", "volatility", "rsi", "bollinger"]

    report = generate_backtest_report(
        engine=result.engine,
        output_dir=tmp_path,
        prefix="readme_test",
        save_graphs=True,
        save_log=True,
        charts=charts,
        formats=("png",),
    )

    # log should exist
    assert Path(report.log_path).exists()

    # each chart should have a png file (main format)
    for chart in charts:
        p = tmp_path / f"readme_test_{chart}.png"
        assert p.exists(), f"Expected {p} to exist"


def test_cli_help_runs():
    # ensure module CLI can be imported and help printed
    completed = subprocess.run([sys.executable, "-m", "back_da_dev", "--help"], capture_output=True)
    assert completed.returncode == 0
    assert b"back_da_dev" in completed.stdout or b"back_da_dev" in completed.stderr
