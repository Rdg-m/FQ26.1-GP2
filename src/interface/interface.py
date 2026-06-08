from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Type, Union

import matplotlib.pyplot as plt
import pandas as pd

from backtesting.backtesting_main import BacktestEngine
from backtesting.modelos_pre_implementados import EMA, MA, buy_and_hold, estrat
from dataprocessing.clean import clean_data
from dataprocessing.load import load_data
from graphing.graphing import (
    plot_drawdown,
    plot_equity_curve,
    plot_cumulative_returns,
    plot_volatility,
    plot_bollinger_bands_chart,
    plot_rsi_chart,
)


STRATEGY_MAP: Dict[str, Type[estrat]] = {
    "buy_and_hold": buy_and_hold,
    "ma": MA,
    "ema": EMA,
}


@dataclass
class BacktestResult:
    engine: BacktestEngine
    metrics: Dict[str, Any]
    graph_paths: Dict[str, str]
    log_path: Optional[str] = None


def list_strategies() -> List[str]:
    """Retorna nomes de estratégias pré-definidas disponíveis."""
    return sorted(STRATEGY_MAP.keys())


def resolve_strategy(
    strategy: Union[str, Type[estrat], estrat],
    initial_capital: float = 10000.0,
    **strategy_kwargs: Any,
) -> estrat:
    """Resolve uma estratégia por nome, classe ou instância."""
    if isinstance(strategy, estrat):
        return strategy

    if isinstance(strategy, str):
        key = strategy.lower()
        if key not in STRATEGY_MAP:
            raise ValueError(f"Estratégia desconhecida: {strategy}. Use {list_strategies()}")
        strategy_cls = STRATEGY_MAP[key]
        return strategy_cls(initial_capital, **strategy_kwargs)

    if isinstance(strategy, type) and issubclass(strategy, estrat):
        return strategy(initial_capital, **strategy_kwargs)

    raise ValueError(
        "strategy deve ser uma string, classe de estratégia ou instância de estrat"
    )


def load_and_clean(
    caminho: Optional[str] = None,
    formato: str = "csv",
    indice: Optional[str] = None,
    fonte: str = "yfinance",
    tempo: str = "10y",
    comeco: Optional[str] = None,
    fim: Optional[str] = None,
    salvar: bool = False,
    de_yfinance: bool = False,
    handle_missing: str = "ffill",
    remove_outliers: bool = False,
    verbose: bool = True,
    clean_kwargs: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """Carrega e limpa dados em um único fluxo."""
    if fonte == "yfinance": de_yfinance = True

    df = load_data(
        caminho=caminho,
        formato=formato,
        indice=indice,
        fonte=fonte,
        tempo=tempo,
        comeco=comeco,
        fim=fim,
        salvar=salvar,
        de_yfinance=de_yfinance,
    )

    if 'symbol' not in df.columns and indice is not None:
        df = df.copy()
        df['symbol'] = indice

    clean_kwargs = clean_kwargs or {}
    cleaned, report = clean_data(
        df,
        handle_missing=handle_missing,
        remove_outliers=remove_outliers,
        verbose=verbose,
        **clean_kwargs,
    )
    if verbose: print(report)
    return cleaned


def build_backtest_engine(
    data: pd.DataFrame,
    symbols: Optional[Sequence[str]] = None,
    initial_capital: float = 10000.0,
    commission: float = 0.001,
    engine_config: Optional[Dict[str, Any]] = None,
    real_data: Optional[bool] = None,
) -> BacktestEngine:
    """Cria e configura o engine de backtest."""
    if symbols is None:
        if 'symbol' not in data.columns:
            raise ValueError(
                "symbols é obrigatório quando os dados não contêm coluna 'symbol'"
            )
        symbols = sorted(data['symbol'].dropna().unique().tolist())

    engine = BacktestEngine(
        data=data,
        symbols=list(symbols),
        initial_capital=initial_capital,
        commission=commission,
    )

    engine_config = engine_config or {}
    if real_data is None:
        engine_config.setdefault('dado_real', True)
    if real_data is not None:
        engine_config['dado_real'] = real_data

    engine._configs.update(engine_config)
    return engine


def compute_backtest_metrics(engine: BacktestEngine) -> Dict[str, Any]:
    """Calcula métricas simples de desempenho a partir da engine."""
    metrics: Dict[str, Any] = {
        'initial_capital': engine.initial_capital,
        'final_cash': float(engine.cash),
        'final_equity': float(engine.portfolio_value),
        'net_return': float(engine.portfolio_value - engine.initial_capital),
        'total_trades': len(engine.closed_positions),
    }

    if engine.initial_capital:
        metrics['return_pct'] = float(
            (engine.portfolio_value - engine.initial_capital)
            / engine.initial_capital
            * 100.0
        )
    else:
        metrics['return_pct'] = 0.0

    if engine.closed_positions:
        wins = [trade for trade in engine.closed_positions if trade.get('net_profit', 0.0) > 0]
        losses = [trade for trade in engine.closed_positions if trade.get('net_profit', 0.0) <= 0]
        metrics['winning_trades'] = len(wins)
        metrics['losing_trades'] = len(losses)
        metrics['win_rate'] = float(len(wins) / max(len(engine.closed_positions), 1) * 100.0)
        metrics['total_profit'] = float(sum(trade.get('net_profit', 0.0) for trade in engine.closed_positions))
    else:
        metrics['winning_trades'] = 0
        metrics['losing_trades'] = 0
        metrics['win_rate'] = 0.0
        metrics['total_profit'] = 0.0

    daily_df = pd.DataFrame(engine.daily_history)
    if not daily_df.empty and 'portfolio_value' in daily_df.columns:
        daily_df = daily_df.sort_values('date')
        peak = daily_df['portfolio_value'].cummax()
        drawdown = (daily_df['portfolio_value'] - peak) / peak
        metrics['max_drawdown_pct'] = float(drawdown.min() * 100.0)

        start = pd.to_datetime(daily_df['date'].iloc[0])
        end = pd.to_datetime(daily_df['date'].iloc[-1])
        duration_days = max((end - start).days, 1)
        metrics['duration_days'] = int(duration_days)

        years = duration_days / 365.0
        if years > 0:
            metrics['annualized_return_pct'] = float(
                ((1.0 + metrics['return_pct'] / 100.0) ** (1.0 / years) - 1.0) * 100.0
            )
        else:
            metrics['annualized_return_pct'] = float(metrics['return_pct'])
    else:
        metrics['max_drawdown_pct'] = 0.0
        metrics['duration_days'] = 0
        metrics['annualized_return_pct'] = 0.0

    return metrics


def save_backtest_log(
    engine: BacktestEngine,
    metrics: Dict[str, Any],
    path: Union[str, Path],
) -> str:
    """Gera um relatório de texto modular em .log."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open('w', encoding='utf-8') as handle:
        handle.write('back_da_dev Backtest Log\n')
        handle.write(f'Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n')
        handle.write(f'Initial Capital: {metrics.get("initial_capital", 0.0):.2f}\n')
        handle.write(f'Final Equity: {metrics.get("final_equity", 0.0):.2f}\n')
        handle.write(f'Return (%): {metrics.get("return_pct", 0.0):.2f}\n')
        handle.write(f'Annualized Return (%): {metrics.get("annualized_return_pct", 0.0):.2f}\n')
        handle.write(f'Max Drawdown (%): {metrics.get("max_drawdown_pct", 0.0):.2f}\n')
        handle.write(f'Total Trades: {metrics.get("total_trades", 0)}\n')
        handle.write(f'Win Rate (%): {metrics.get("win_rate", 0.0):.2f}\n')
        handle.write(f'Total Profit: {metrics.get("total_profit", 0.0):.2f}\n')

        if engine.closed_positions:
            handle.write('\nTrade History:\n')
            for trade in engine.closed_positions:
                handle.write(
                    f"{trade.get('symbol')} {trade.get('entry_date')} -> {trade.get('exit_date')} "
                    f"qty={trade.get('quantity')} profit={trade.get('net_profit', 0.0):.2f} "
                    f"reason={trade.get('exit_reason')}\n"
                )

    return str(path)


def export_backtest_graphs(
    engine: BacktestEngine,
    output_dir: Union[str, Path] = './results',
    prefix: str = 'backtest',
    charts: Optional[Sequence[str]] = None,
    formats: Sequence[str] = ('png', 'svg'),
) -> Dict[str, str]:
    """Gera gráficos automáticos a partir do histórico diário.

    Parameters
    - charts: lista de nomes de gráficos a gerar. Se None, gera todos suportados.
    - formats: extensões/formatos de saída (ex: ('png','svg')).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # mapa de gráficos suportados para funções e tipo de entrada
    supported = {
        'equity_curve': ('daily_history', plot_equity_curve),
        'drawdown': ('daily_history', plot_drawdown),
        'cumulative_returns': ('price_series', plot_cumulative_returns),
        'volatility': ('price_series', plot_volatility),
        'bollinger': ('price_series', plot_bollinger_bands_chart),
        'rsi': ('price_series', plot_rsi_chart),
    }

    default_charts = list(supported.keys())
    charts = list(charts) if charts is not None else default_charts

    graph_paths: Dict[str, str] = {}

    # preparar price_series a partir do daily_history quando possível
    daily_df = pd.DataFrame(engine.daily_history)
    price_series = None
    if not daily_df.empty:
        if 'date' in daily_df.columns:
            try:
                daily_df = daily_df.sort_values('date')
                daily_df.index = pd.to_datetime(daily_df['date'])
            except Exception:
                pass

        for col in ('close', 'price', 'portfolio_value'):
            if col in daily_df.columns:
                price_series = pd.Series(daily_df[col].values, index=daily_df.index, name=col)
                break

    for chart in charts:
        if chart not in supported:
            print(f"Warning: gráfico desconhecido '{chart}', pulando.")
            continue

        input_type, func = supported[chart]
        try:
            if input_type == 'daily_history':
                ax = func(engine.daily_history)
            else:
                if price_series is None or price_series.empty:
                    print(f"Warning: sem série de preços disponível para '{chart}', pulando.")
                    continue
                ax = func(price_series)

            fig = ax.figure
            for i, fmt in enumerate(formats):
                out_path = output_dir / f"{prefix}_{chart}.{fmt}"
                fig.savefig(out_path, bbox_inches='tight')
                # registrar o primeiro formato como caminho principal
                if i == 0:
                    graph_paths[chart] = str(out_path)
                else:
                    graph_paths[f"{chart}_{fmt}"] = str(out_path)
            plt.close(fig)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Erro ao gerar gráfico '{chart}': {exc}")

    return graph_paths


def generate_backtest_report(
    engine: BacktestEngine,
    output_dir: Union[str, Path] = './results',
    prefix: str = 'backtest',
    save_graphs: bool = True,
    save_log: bool = True,
    charts: Optional[Sequence[str]] = None,
    formats: Sequence[str] = ('png', 'svg'),
) -> BacktestResult:
    """Gera um relatório completo de backtest com gráficos e .log."""
    metrics = compute_backtest_metrics(engine)
    graph_paths: Dict[str, str] = {}
    log_path: Optional[str] = None

    if save_graphs:
        graph_paths = export_backtest_graphs(
            engine, output_dir=output_dir, prefix=prefix, charts=charts, formats=formats
        )

    if save_log:
        log_path = save_backtest_log(
            engine,
            metrics,
            Path(output_dir) / f'{prefix}.log',
        )

    return BacktestResult(
        engine=engine,
        metrics=metrics,
        graph_paths=graph_paths,
        log_path=log_path,
    )


def run_standard_backtest(
    data: Optional[pd.DataFrame] = None,
    symbols: Optional[Sequence[str]] = None,
    strategy: Union[str, Type[estrat], estrat] = 'buy_and_hold',
    initial_capital: float = 10000.0,
    commission: float = 0.001,
    engine_config: Optional[Dict[str, Any]] = None,
    strategy_kwargs: Optional[Dict[str, Any]] = None,
    load_kwargs: Optional[Dict[str, Any]] = None,
    clean_kwargs: Optional[Dict[str, Any]] = None,
    output_dir: Union[str, Path] = './results',
    save_log: bool = True,
    save_graphs: bool = True,
    charts: Optional[Sequence[str]] = None,
    chart_formats: Sequence[str] = ('png', 'svg'),
) -> BacktestResult:
    """Executa um backtest padrão e retorna resultados e caminhos de saída."""
    load_kwargs = load_kwargs or {}
    clean_kwargs = clean_kwargs or {}
    strategy_kwargs = strategy_kwargs or {}

    if data is None:
        data = load_and_clean(**load_kwargs, clean_kwargs=clean_kwargs)
    elif clean_kwargs:
        cleaned = clean_data(data, **clean_kwargs)
        if isinstance(cleaned, tuple):
            data, _ = cleaned
        else:
            data = cleaned

    engine = build_backtest_engine(
        data=data,
        symbols=symbols,
        initial_capital=initial_capital,
        commission=commission,
        engine_config=engine_config,
    )

    strategy_instance = resolve_strategy(
        strategy,
        initial_capital,
        **strategy_kwargs,
    )
    engine.run(strategy_instance)

    metrics = compute_backtest_metrics(engine)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    graph_paths: Dict[str, str] = {}
    log_path: Optional[str] = None

    if save_graphs:
        graph_paths = export_backtest_graphs(
            engine,
            output_dir=output_dir,
            prefix='backtest',
            charts=charts,
            formats=chart_formats,
        )

    if save_log:
        log_path = save_backtest_log(
            engine,
            metrics,
            output_dir / 'backtest.log',
        )

    return BacktestResult(
        engine=engine,
        metrics=metrics,
        graph_paths=graph_paths,
        log_path=log_path,
    )


def main() -> int:
    """CLI mínimo que usa o hub de interface em um fluxo padrão."""
    parser = argparse.ArgumentParser(
        description='back_da_dev - backtest financial strategy hub',
    )
    parser.add_argument('--indice', help='símbolo do ativo para carregar via yfinance')
    parser.add_argument('--symbols', nargs='+', help='lista de símbolos para o backtest')
    parser.add_argument('--strategy', default='buy_and_hold', help='nome da estratégia (buy_and_hold, ma, ema)')
    parser.add_argument('--initial-capital', type=float, default=10000.0, help='capital inicial')
    parser.add_argument('--commission', type=float, default=0.001, help='taxa de corretagem por operação')
    parser.add_argument('--output-dir', default='./results', help='diretório para salvar gráficos e relatório')
    parser.add_argument('--no-graphs', action='store_false', dest='save_graphs', help='não gerar gráficos automáticos')
    parser.add_argument('--no-log', action='store_false', dest='save_log', help='não gerar arquivo .log')
    parser.add_argument('--tempo', default='10y', help='período para yfinance')
    parser.add_argument('--fonte', default='yfinance', help='fonte de dados')
    parser.add_argument('--caminho', help='arquivo local de dados')
    parser.add_argument('--formato', default='csv', help='formato do arquivo local')
    parser.add_argument('--de-yfinance', action='store_true', help='desfaz o MultiIndex do yfinance quando aplicável')
    parser.add_argument('--charts', nargs='+', help='lista de gráficos a gerar (ex: equity_curve drawdown rsi)')
    parser.add_argument('--chart-formats', nargs='+', default=['png','svg'], help='formatos de saída para os gráficos')
    args = parser.parse_args()

    if not args.indice and not args.caminho:
        parser.error('Informe --indice ou --caminho para carregar dados')

    load_kwargs = {
        'indice': args.indice,
        'fonte': args.fonte,
        'tempo': args.tempo,
        'caminho': args.caminho,
        'formato': args.formato,
        'de_yfinance': args.de_yfinance,
    }

    symbols = args.symbols or ([args.indice] if args.indice else None)
    result = run_standard_backtest(
        symbols=symbols,
        strategy=args.strategy,
        initial_capital=args.initial_capital,
        commission=args.commission,
        load_kwargs=load_kwargs,
        output_dir=args.output_dir,
        save_graphs=args.save_graphs,
        save_log=args.save_log,
        charts=args.charts,
        chart_formats=args.chart_formats,
    )

    print(f'Backtest finalizado. Equity final: {result.metrics["final_equity"]:.2f}')
    if result.log_path:
        print(f'Relatório salvo em {result.log_path}')
    for name, path in result.graph_paths.items():
        print(f'{name}: {path}')

    return 0

