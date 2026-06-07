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
    dates = pd.date_range(start="2025-01-01", periods=3, freq="B")
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
    """Testa a execução básica usando dados falsos rápidos (Unit Test)."""
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
    """Testa se o gerador de relatórios cria os logs e PNGs."""
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

    # Corrigido: Usando a assinatura real da nossa interface.py
    report = generate_backtest_report(
        engine=result.engine,
        output_dir=tmp_path,
        prefix="readme_test",
        save_graphs=True,
        save_log=True,
    )

    # O arquivo .log deve existir
    assert Path(report.log_path).exists()

    # Os gráficos gerados pela nossa interface atual (equity_curve e drawdown) devem existir
    charts_esperados = ["equity_curve", "drawdown"]
    for chart in charts_esperados:
        p = tmp_path / f"readme_test_{chart}.png"
        assert p.exists(), f"Esperava que o arquivo {p} existisse"


def test_yfinance_integration(tmp_path):
    """
    Testa a integração real com o Yahoo Finance citada no README (Integration Test).
    Pede apenas 5 dias para não atrasar a esteira de testes.
    """
    result = run_standard_backtest(
        strategy="buy_and_hold",
        initial_capital=10000.0,
        commission=0.001,
        # A Mágica acontece aqui: passando load_kwargs em vez de data=df
        load_kwargs={"indice": "PETR4.SA", "fonte": "yfinance", "tempo": "5d"},
        output_dir=tmp_path,
        save_graphs=False,
        save_log=False,
    )

    assert result is not None
    assert result.metrics["final_equity"] > 0
    assert result.metrics["total_trades"] >= 0


def test_cli_help_runs():
    """Garante que o comando de terminal funciona sem quebrar."""
    completed = subprocess.run([sys.executable, "-m", "back_da_dev", "--help"], capture_output=True)
    assert completed.returncode == 0
    assert b"back_da_dev" in completed.stdout or b"back_da_dev" in completed.stderr