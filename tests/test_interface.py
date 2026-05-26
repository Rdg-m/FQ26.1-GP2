import pandas as pd

from back_da_dev import run_standard_backtest, list_strategies


def test_interface_run_standard_backtest(tmp_path):
    dates = pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"])
    data = pd.DataFrame(
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

    result = run_standard_backtest(
        data=data,
        symbols=["A"],
        strategy="buy_and_hold",
        initial_capital=1000.0,
        commission=0.0,
        output_dir=tmp_path,
        save_log=True,
        save_graphs=True,
    )

    assert result.engine.portfolio_value >= 0
    assert result.log_path is not None
    assert tmp_path.joinpath("backtest.log").exists()
    assert "equity_curve" in result.graph_paths
    assert "drawdown" in result.graph_paths
    assert result.metrics["total_trades"] == 0
    assert "buy_and_hold" in list_strategies()
