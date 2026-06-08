import functools
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DEFAULT_COLOR_PALETTE = [
    '#1f77b4',  # azul
    '#ff7f0e',  # laranja
    '#2ca02c',  # verde
    '#d62728',  # vermelho
    '#9467bd',  # roxo
    '#8c564b',  # marrom
    '#e377c2',  # rosa
    '#7f7f7f',  # cinza
    '#bcbd22',  # oliva
    '#17becf',  # ciano
]

DEFAULT_THEME_MAP = {
    'dark': {
        'figure.facecolor': '#212121',
        'axes.facecolor': '#222222',
        'axes.edgecolor': '#FFFFFF',
        'axes.labelcolor': '#FFFFFF',
        'xtick.color': '#FFFFFF',
        'ytick.color': '#FFFFFF',
        'text.color': '#FFFFFF',
        'grid.color': '#555555',
    },
    'light': {
        'figure.facecolor': '#FFFFFF',
        'axes.facecolor': '#F6F6F6',
        'axes.edgecolor': '#222222',
        'axes.labelcolor': '#222222',
        'xtick.color': '#222222',
        'ytick.color': '#222222',
        'text.color': '#222222',
        'grid.color': '#DDDDDD',
    },
    'seaborn': {
        'figure.facecolor': '#FFFFFF',
        'axes.facecolor': '#FFFFFF',
        'axes.edgecolor': '#333333',
        'axes.labelcolor': '#333333',
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'text.color': '#333333',
        'grid.color': '#DDDDDD',
    },
}


def _apply_theme(theme: str = 'dark') -> None:
    """Configura o estilo base do Matplotlib para o tema desejado."""
    theme = theme.lower() if isinstance(theme, str) else 'dark'
    style = DEFAULT_THEME_MAP.get(theme, DEFAULT_THEME_MAP['dark'])
    plt.rcParams.update(style)
    plt.rcParams.update({'grid.linestyle': '--', 'grid.alpha': 0.35, 'font.size': 10})


def _normalize_color_palette(colors: Optional[Sequence[str]], count: int) -> Sequence[str]:
    """Normaliza a paleta de cores para ter ao menos `count` entradas."""
    if colors is None:
        colors = DEFAULT_COLOR_PALETTE
    colors = list(colors)
    if len(colors) >= count:
        return colors[:count]
    return (colors * ((count // len(colors)) + 1))[:count]


def _extract_axes(result: Any) -> plt.Axes:
    if isinstance(result, tuple) and len(result) >= 1:
        candidate = result[-1]
        if isinstance(candidate, plt.Axes):
            return candidate
    if isinstance(result, plt.Axes):
        return result
    return plt.gca()


def apply_plot_style(
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    legend: bool = True,
    legend_loc: str = 'best',
    colors: Optional[Sequence[str]] = None,
    grid: bool = True,
    theme: str = 'dark',
    figsize: Tuple[float, float] = (12.0, 6.0),
    dpi: int = 150,
    title_fontsize: int = 16,
    label_fontsize: int = 12,
    tick_fontsize: int = 10,
    legend_fontsize: int = 10,
    grid_kwargs: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorador que aplica formatação customizada em um gráfico Matplotlib."""

    def decorator(plot_func: Callable[..., Any]) -> Callable[..., Any]:

        @functools.wraps(plot_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _apply_theme(theme)
            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
            kwargs.setdefault('ax', ax)

            result = plot_func(*args, **kwargs)
            if result is not None and isinstance(result, tuple) and isinstance(result[-1], plt.Axes):
                ax = result[-1]
            elif isinstance(result, plt.Axes):
                ax = result

            if title:
                ax.set_title(title, fontsize=title_fontsize, pad=14)
            if subtitle:
                fig.suptitle(subtitle, fontsize=title_fontsize - 2, alpha=0.85)
            if xlabel:
                ax.set_xlabel(xlabel, fontsize=label_fontsize)
            if ylabel:
                ax.set_ylabel(ylabel, fontsize=label_fontsize)

            ax.tick_params(axis='both', labelsize=tick_fontsize)
            if grid:
                grid_options = {'linestyle': '--', 'linewidth': 0.75, 'alpha': 0.4}
                if grid_kwargs:
                    grid_options.update(grid_kwargs)
                ax.grid(True, **grid_options)

            if legend:
                legend_obj = ax.legend(loc=legend_loc, fontsize=legend_fontsize)
                if legend_obj is not None:
                    legend_obj.get_frame().set_alpha(0.85)

            return ax

        return wrapper

    return decorator


def calculate_rsi(price_series: Union[pd.Series, Sequence[float]], period: int = 14) -> pd.Series:
    """Retorna o índice RSI como série de pandas."""
    prices = pd.Series(price_series, dtype='float64')
    delta = prices.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)

    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.fillna(50.0)


def calculate_macd(
    price_series: Union[pd.Series, Sequence[float]],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calcula MACD, linha de sinal e histograma para uma série de preços."""
    prices = pd.Series(price_series, dtype='float64')
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(
    price_series: Union[pd.Series, Sequence[float]],
    period: int = 20,
    std_multiplier: float = 2.0,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Retorna a média móvel central, banda superior e banda inferior."""
    prices = pd.Series(price_series, dtype='float64')
    middle_band = prices.rolling(window=period, min_periods=period).mean()
    rolling_std = prices.rolling(window=period, min_periods=period).std(ddof=0)

    upper_band = middle_band + rolling_std * std_multiplier
    lower_band = middle_band - rolling_std * std_multiplier
    return middle_band, upper_band, lower_band


def calculate_discrete_yields(
    price_series: Union[pd.Series, Sequence[float]],
    fill_method: Optional[str] = None,
) -> pd.Series:
    """Calcula yields discretos (retornos percentuais) entre períodos consecutivos."""
    prices = pd.Series(price_series, dtype='float64')
    yields = prices.pct_change(fill_method=fill_method)
    return yields


def discrete_to_continuous(
    discrete_returns: Union[pd.Series, Sequence[float], np.ndarray]
) -> Union[pd.Series, np.ndarray]:
    """Transforma retornos discretos em retornos contínuos por logaritmo natural."""
    if isinstance(discrete_returns, pd.Series):
        return np.log1p(discrete_returns).rename(discrete_returns.name)
    return np.log1p(np.asarray(discrete_returns, dtype='float64'))


def generate_sample_time_series(
    length: int = 120,
    start: float = 100.0,
    drift: float = 0.0008,
    volatility: float = 0.01,
    seed: Optional[int] = 42,
) -> pd.Series:
    """Gera uma série temporal simulada de preços usando um passeio aleatório com drift."""
    rng = np.random.default_rng(seed)
    returns = rng.normal(loc=drift, scale=volatility, size=length)
    prices = start * np.exp(np.cumsum(returns))
    index = pd.date_range(end=pd.Timestamp.today(), periods=length, freq='B')
    return pd.Series(prices, index=index, name='Preço Simulado')


@apply_plot_style(
    title='Série Temporal de Preço Simulado',
    xlabel='Data',
    ylabel='Preço',
    legend=True,
    legend_loc='upper left',
    theme='light',
    figsize=(14.0, 6.0),
)
def plot_time_series(
    series: Union[pd.Series, Sequence[float]],
    label: str = 'Preço',
    ax: Optional[plt.Axes] = None,
    colors: Optional[Sequence[str]] = None,
    line_style: str = '-',
    marker: Optional[str] = None,
) -> plt.Axes:
    """Plota uma série temporal de preços usando Matplotlib."""
    values = pd.Series(series, dtype='float64')
    if colors is None:
        colors = _normalize_color_palette(None, 1)
    ax = ax if ax is not None else plt.gca()
    ax.plot(values.index, values.values, label=label, color=colors[0], linestyle=line_style, marker=marker)
    return ax


__all__ = [
    'apply_plot_style',
    'calculate_rsi',
    'calculate_macd',
    'calculate_bollinger_bands',
    'calculate_discrete_yields',
    'discrete_to_continuous',
    'generate_sample_time_series',
    'plot_time_series',
]
@apply_plot_style(
    title='Curva de Patrimônio (Equity Curve)',
    xlabel='Data',
    ylabel='Capital Total (R$)',
    legend=True,
    theme='dark',
    figsize=(14.0, 7.0)
)
def plot_equity_curve(
    daily_history: list,
    ax: Optional[plt.Axes] = None,
    colors: Optional[Sequence[str]] = None
) -> plt.Axes:
    df_history = pd.DataFrame(daily_history)
    
    if df_history.empty or 'date' not in df_history.columns or 'portfolio_value' not in df_history.columns:
        print("Dados de histórico diário insuficientes para gerar a Equity Curve.")
        return plt.gca()

    if colors is None:
        colors = _normalize_color_palette(None, 2)
    
    ax = ax if ax is not None else plt.gca()
    
    # Plota a linha principal do patrimônio
    ax.plot(
        df_history['date'], 
        df_history['portfolio_value'], 
        label='Valor do Portfolio', 
        color=colors[0], 
        linewidth=2.0
    )
    # Dinheiro em caixa
    if 'cash' in df_history.columns:
        ax.plot(
            df_history['date'], 
            df_history['cash'], 
            label='Dinheiro em Caixa', 
            color=colors[1], 
            linestyle='--', 
            alpha=0.6 
        )
        
    return ax

@apply_plot_style(
    title='Gráfico de Drawdown (Quedas do Patrimônio)',
    xlabel='Data',
    ylabel='Drawdown (%)',
    legend=True,
    theme='dark',
    figsize=(14.0, 5.0)
)
def plot_drawdown(
    daily_history: list,
    ax: Optional[plt.Axes] = None,
    colors: Optional[Sequence[str]] = None
) -> plt.Axes:
    """
    Desenha o gráfico de Drawdown 
    """
    df_history = pd.DataFrame(daily_history)
    
    if df_history.empty or 'date' not in df_history.columns or 'portfolio_value' not in df_history.columns:
        print("\nDados insuficientes para gerar o Drawdown")
        return plt.gca()

    picos_acumulados = df_history['portfolio_value'].cummax()
    drawdowns = (df_history['portfolio_value'] - picos_acumulados) / picos_acumulados * 100.0

    if colors is None:
        colors = _normalize_color_palette(None, 4)
    
    ax = ax if ax is not None else plt.gca()
    
    ax.fill_between(
        df_history['date'],
        drawdowns,
        0,
        color=colors[3], 
        alpha=0.4,
        label='Drawdown (%)'
    )
    
    ax.plot(df_history['date'], drawdowns, color=colors[3], linewidth=1.5)
    
    return ax

def calculate_var(returns: Union[pd.Series, Sequence[float]], confidence_level: float = 0.05) -> float:
    """
    Calcula o Value at Risk (VaR) histórico para a série de retornos.
    Retorna a pior queda esperada para o nível de confiança
    """
    ret_series = pd.Series(returns).dropna()
    if ret_series.empty:
        return 0.0
    var = np.percentile(ret_series, confidence_level * 100)
    return float(var)

def calculate_cvar(returns: Union[pd.Series, Sequence[float]], confidence_level: float = 0.05) -> float:
    """
    Calcula o CVar
    """
    ret_series = pd.Series(returns).dropna()
    if ret_series.empty:
        return 0.0
    
    var_threshold = calculate_var(ret_series, confidence_level)
    piores_retornos = ret_series[ret_series <= var_threshold]
    if piores_retornos.empty:
        return float(var_threshold)
    return float(piores_retornos.mean())

@apply_plot_style(
    title='Retorno Acumulado (%)',
    xlabel='Data',
    ylabel='Retorno (%)',
    legend=True,
    theme='dark',
    figsize=(14.0, 6.0)
)

def plot_cumulative_returns(
    price_series: pd.Series, 
    ax: Optional[plt.Axes] = None, 
    colors: Optional[Sequence[str]] = None
) -> plt.Axes:
    """
    Plota o retorno acumulado percentual 
    """
    retornos_diarios = calculate_discrete_yields(price_series).fillna(0)
    retorno_acumulado = (1 + retornos_diarios).cumprod() - 1
    retorno_acumulado_pct = retorno_acumulado * 100.0
    
    if colors is None:
        colors = _normalize_color_palette(None, 4) 
    ax = ax if ax is not None else plt.gca()
    
    ax.plot(
        retorno_acumulado_pct.index, 
        retorno_acumulado_pct.values, 
        color=colors[2], # Verde
        linewidth=2.0,
        label='Retorno Acumulado'
    )
    
    ax.fill_between(
        retorno_acumulado_pct.index, 
        retorno_acumulado_pct.values, 
        0, 
        where=(retorno_acumulado_pct.values >= 0), 
        color=colors[2], 
        alpha=0.2
    )
    ax.fill_between(
        retorno_acumulado_pct.index, 
        retorno_acumulado_pct.values, 
        0, 
        where=(retorno_acumulado_pct.values < 0), 
        color=colors[3], # Vermelho 
        alpha=0.2
    )
    
    return ax

@apply_plot_style(
    title='Volatilidade Móvel Anualizada (Risco)',
    xlabel='Data',
    ylabel='Volatilidade Anualizada (%)',
    legend=True,
    theme='dark',
    figsize=(14.0, 5.0)
)

def plot_volatility(
    price_series: pd.Series, 
    window: int = 20, 
    ax: Optional[plt.Axes] = None, 
    colors: Optional[Sequence[str]] = None
) -> plt.Axes:
    """
    Calcula e plota a volatilidade móvel
    """
    retornos_diarios = calculate_discrete_yields(price_series)
    
    volatilidade_movel = retornos_diarios.rolling(window=window).std() * np.sqrt(252) * 100.0
    
    if colors is None:
        colors = _normalize_color_palette(None, 5) 
    ax = ax if ax is not None else plt.gca()
    
    ax.plot(
        volatilidade_movel.index, 
        volatilidade_movel.values, 
        color=colors[4],
        linewidth=1.5,
        label=f'Volatilidade ({window} dias)'
    )
    
    return ax

@apply_plot_style(
    title='Análise Técnica: Preço e Bandas de Bollinger',
    xlabel='Data',
    ylabel='Preço (R$)',
    legend=True,
    theme='dark',
    figsize=(14.0, 7.0)
)
def plot_bollinger_bands_chart(
    price_series: pd.Series,
    period: int = 20,
    ax: Optional[plt.Axes] = None,
    colors: Optional[Sequence[str]] = None
) -> plt.Axes:
    """
    Desenha o gráfico de preços com as Bandas de Bollinger
    """
    middle, upper, lower = calculate_bollinger_bands(price_series, period=period)
    
    if colors is None:
        colors = _normalize_color_palette(None, 4)
    ax = ax if ax is not None else plt.gca()
    
    ax.plot(price_series.index, price_series.values, label='Preço', color='#ffffff', linewidth=1.5)
    
    ax.plot(upper.index, upper.values, label='Banda Superior', color=colors[0], linestyle='--', alpha=0.6)
    ax.plot(lower.index, lower.values, label='Banda Inferior', color=colors[0], linestyle='--', alpha=0.6)
    ax.plot(middle.index, middle.values, label='Média Móvel', color=colors[1], linestyle=':', alpha=0.8)
    
    ax.fill_between(price_series.index, lower.values, upper.values, color=colors[0], alpha=0.1)
    
    return ax

@apply_plot_style(
    title='Índice de Força Relativa (RSI)',
    xlabel='Data',
    ylabel='RSI',
    legend=True,
    theme='dark',
    figsize=(14.0, 4.0) # Mais baixinho para ficar embaixo do gráfico de preço
)
def plot_rsi_chart(
    price_series: pd.Series,
    period: int = 14,
    ax: Optional[plt.Axes] = None,
    colors: Optional[Sequence[str]] = None
) -> plt.Axes:
    """
    Desenha o RSI 
    """
    rsi = calculate_rsi(price_series, period=period)
    
    if colors is None:
        colors = _normalize_color_palette(None, 5)
    ax = ax if ax is not None else plt.gca()
    
    ax.plot(rsi.index, rsi.values, label=f'RSI ({period})', color=colors[4], linewidth=1.5)
    
    ax.axhline(70, color=colors[3], linestyle='--', alpha=0.6, label='Sobrecomprado (70)')
    ax.axhline(30, color=colors[2], linestyle='--', alpha=0.6, label='Sobrevendido (30)')
    
    ax.fill_between(rsi.index, 70, 30, color='#7f7f7f', alpha=0.1)
    
    ax.set_ylim(0, 100) 
    return ax


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate_annual: float = 0.0) -> float:
    """Calcula o Índice de Sharpe Anualizado com base nos retornos diários."""
    ret_series = pd.Series(returns).dropna()
    if ret_series.empty or ret_series.std() == 0:
        return 0.0
    
    rf_daily = (1 + risk_free_rate_annual) ** (1/252) - 1
    excess_returns = ret_series - rf_daily
    return float((excess_returns.mean() / excess_returns.std()) * np.sqrt(252))


def calculate_sortino_ratio(returns: pd.Series, risk_free_rate_annual: float = 0.0) -> float:
    """Calcula o Índice de Sortino Anualizado."""
    ret_series = pd.Series(returns).dropna()
    if ret_series.empty:
        return 0.0
        
    rf_daily = (1 + risk_free_rate_annual) ** (1/252) - 1
    excess_returns = ret_series - rf_daily
    downside_returns = excess_returns[excess_returns < 0]
    
    if downside_returns.empty or downside_returns.std() == 0:
        return 0.0 
        
    downside_volatility = downside_returns.std() * np.sqrt(252)
    annualized_return = excess_returns.mean() * 252
    return float(annualized_return / downside_volatility)


def generate_performance_summary(daily_history: list, closed_positions: list = None) -> pd.DataFrame:
    """
    Compila todas as métricas em uma tabela.
    """
    df = pd.DataFrame(daily_history)
    if df.empty or 'portfolio_value' not in df.columns:
        return pd.DataFrame()
        
    capital_inicial = float(df['portfolio_value'].iloc[0])
    capital_final = float(df['portfolio_value'].iloc[-1])
    total_dias = len(df)
    
    retorno_total = ((capital_final - capital_inicial) / capital_inicial) * 100
    retornos_diarios = df['portfolio_value'].pct_change().dropna()
    
    retorno_anualizado = 0.0
    vol_anualizada = 0.0
    var_95 = 0.0
    cvar_95 = 0.0
    sharpe = 0.0
    sortino = 0.0
    
    if not retornos_diarios.empty:
        retorno_anualizado = (((capital_final / capital_inicial) ** (252 / total_dias)) - 1) * 100
        vol_anualizada = retornos_diarios.std() * np.sqrt(252) * 100
        var_95 = calculate_var(retornos_diarios) * 100
        cvar_95 = calculate_cvar(retornos_diarios) * 100
        sharpe = calculate_sharpe_ratio(retornos_diarios)
        sortino = calculate_sortino_ratio(retornos_diarios)

    picos = df['portfolio_value'].cummax()
    drawdowns = (df['portfolio_value'] - picos) / picos * 100
    max_drawdown = drawdowns.min()
    avg_drawdown = drawdowns[drawdowns < 0].mean() if (drawdowns < 0).any() else 0.0
    
    max_dd_duration = 0
    current_dd_duration = 0
    for dd in drawdowns:
        if dd < 0:
            current_dd_duration += 1
            max_dd_duration = max(max_dd_duration, current_dd_duration)
        else:
            current_dd_duration = 0

    dias_ganho = int((retornos_diarios > 0).sum())
    
    win_streak = current_win = 0
    loss_streak = current_loss = 0
    for r in retornos_diarios:
        if r > 0:
            current_win += 1
            win_streak = max(win_streak, current_win)
            current_loss = 0
        elif r < 0:
            current_loss += 1
            loss_streak = max(loss_streak, current_loss)
            current_win = 0

    total_trades = 0
    win_rate = 0.0
    profit_factor = 0.0
    lucro_medio = 0.0
    risk_reward_ratio = 0.0
    
    if closed_positions and len(closed_positions) > 0:
        df_trades = pd.DataFrame(closed_positions)
        total_trades = len(df_trades)
        
        if 'profit' in df_trades.columns:
            trades_vencedores = df_trades[df_trades['profit'] > 0]
            trades_perdedores = df_trades[df_trades['profit'] < 0]
            
            win_rate = (len(trades_vencedores) / total_trades) * 100 if total_trades > 0 else 0.0
            lucro_medio = df_trades['profit'].mean()
            
            lucro_bruto = trades_vencedores['profit'].sum()
            prejuizo_bruto = abs(trades_perdedores['profit'].sum())
            profit_factor = (lucro_bruto / prejuizo_bruto) if prejuizo_bruto > 0 else float('inf')
            
            avg_gain = trades_vencedores['profit'].mean() if len(trades_vencedores) > 0 else 0.0
            avg_loss = abs(trades_perdedores['profit'].mean()) if len(trades_perdedores) > 0 else 0.0
            risk_reward_ratio = (avg_gain / avg_loss) if avg_loss > 0 else float('inf')

    metrics_manifest = {
        'Métrica': [
            'Capital Inicial', 'Capital Final', 'Retorno Total (%)', 'Retorno Anualizado (%)',
            'Volatilidade Anualizada (%)', 'Índice de Sharpe', 'Índice de Sortino',
            'Drawdown Máximo (%)', 'Drawdown Médio (%)', 'Duração Máxima do Drawdown (Dias)',
            'Total de Trades Executados', 'Taxa de Ganho (Win Rate)', 'Fator de Lucro (Profit Factor)',
            'Lucro Médio por Trade (R$)', 'Razão Média Ganho/Perda (Risk/Reward)',
            'Dias Úteis Positivos', 'Maior Sequência de Ganhos (Win Streak)', 'Maior Sequência de Perdas (Loss Streak)',
            'VaR Histórico 95% Diário (%)', 'CVaR Histórico 95% Diário (%)'
        ],
        'Valor': [
            f"R$ {capital_inicial:,.2f}", f"R$ {capital_final:,.2f}", f"{retorno_total:.2f}%", f"{retorno_anualizado:.2f}%",
            f"{vol_anualizada:.2f}%", f"{sharpe:.2f}", f"{sortino:.2f}",
            f"{max_drawdown:.2f}%", f"{avg_drawdown:.2f}%", f"{max_dd_duration} dias",
            f"{total_trades}", f"{win_rate:.1f}%", f"{profit_factor:.2f}",
            f"R$ {lucro_medio:,.2f}", f"{risk_reward_ratio:.2f}",
            f"{dias_ganho} de {len(retornos_diarios)} dias", f"{win_streak} dias", f"{loss_streak} dias",
            f"{var_95:.2f}%", f"{cvar_95:.2f}%"
        ]
    }
    
    return pd.DataFrame(metrics_manifest).set_index('Métrica')
if __name__ == '__main__':
   # teste de sanidade
    series = generate_sample_time_series(length=30)
    plot_time_series(series, label='Série de Preço', colors=['#d62728'], line_style='-', marker='o')
    plt.show()