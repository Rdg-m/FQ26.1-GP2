import pandas as pd

from back_da_dev import run_standard_backtest, list_strategies
from dataprocessing.load import _flatten_yfinance_columns, load_data


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
    # novos gráficos esperados (gerados por padrão)
    assert "cumulative_returns" in result.graph_paths
    assert "volatility" in result.graph_paths
    # verificar arquivos físicos (formato png padrão)
    assert tmp_path.joinpath("backtest_cumulative_returns.png").exists()
    assert tmp_path.joinpath("backtest_volatility.png").exists()
    assert result.metrics["total_trades"] == 0
    assert "buy_and_hold" in list_strategies()


def test_flatten_yfinance_columns_single_ticker():
    columns = pd.MultiIndex.from_arrays(
        [
            ["Open", "High", "Low", "Close", "Volume"],
            ["AAPL", "AAPL", "AAPL", "AAPL", "AAPL"],
        ]
    )
    df = pd.DataFrame(
        [[100.0, 101.0, 99.5, 101.0, 1000], [102.0, 103.0, 101.5, 103.0, 1100]],
        columns=columns,
        index=pd.to_datetime(["2025-01-01", "2025-01-02"]),
    )

    cleaned = _flatten_yfinance_columns(df)

    assert not isinstance(cleaned.columns, pd.MultiIndex)
    assert list(cleaned.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert cleaned.loc[pd.Timestamp("2025-01-01"), "Open"] == 100.0


def test_load_data_de_yfinance_flattens_multiindex(monkeypatch):
    columns = pd.MultiIndex.from_arrays(
        [
            ["Open", "High", "Low", "Close", "Volume"],
            ["AAPL", "AAPL", "AAPL", "AAPL", "AAPL"],
        ]
    )
    df = pd.DataFrame(
        [[100.0, 101.0, 99.5, 101.0, 1000], [102.0, 103.0, 101.5, 103.0, 1100]],
        columns=columns,
        index=pd.to_datetime(["2025-01-01", "2025-01-02"]),
    )

    monkeypatch.setattr('dataprocessing.load.yf', type('obj', (), {'download': staticmethod(lambda *args, **kwargs: df)}))

    loaded = load_data(indice='AAPL', fonte='yfinance', de_yfinance=True)

    assert not isinstance(loaded.columns, pd.MultiIndex)
    assert list(loaded.columns) == ["Open", "High", "Low", "Close", "Volume"]
