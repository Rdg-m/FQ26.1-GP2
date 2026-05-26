"""
Módulo de Geração de Gráficos e Visualizações de Resultados

RESPONSABILIDADES:
- Criar visualizações dos resultados do backtest
- Gerar gráficos de desempenho da estratégia
- Produzir tabelas de resumo de resultados
- Exportar relatórios em múltiplos formatos
- Fornecer formatação profissional para apresentação

TIPOS DE GRÁFICOS SUPORTADOS:

1. GRÁFICOS DE DESEMPENHO
   - Equity Curve: Evolução do patrimônio ao longo do tempo
   - Drawdown Chart: Quedas em relação ao pico anterior
   - Returns Over Time: Retorno acumulado (%)
   - Underwater Plot: Visualiza drawdown em relação ao máximo

2. GRÁFICOS DE ANÁLISE TÉCNICA
   - Price Chart: Gráfico de preços (candlestick, linha)
   - Moving Averages: Médias móveis sobrepostas ao preço
   - Technical Indicators: RSI, MACD, Bollinger Bands, etc.

3. GRÁFICOS DE DISTRIBUIÇÃO
   - Histograma de Returns: Distribuição de retornos
   - Risk-Return Scatter: Risco vs Retorno esperado
   - Correlation Matrix: Correlação entre ativos

4. GRÁFICOS DE OPERAÇÕES
   - Trade Log: Histórico de trades (entradas/saídas)
   - Win/Loss Distribution: Distribuição de trades ganhos/perdidos
   - Performance by Month: Retorno por mês (heatmap)

5. GRÁFICOS ADICIONAIS
   - Gráficos de Pizza (Allocação de portfolio)
   - Gráficos de Barras (Comparação de métricas)
   - Gráficos de Linhas (Múltiplas séries temporais)

ELEMENTOS DE FORMATAÇÃO:

Títulos e Legendas:
- Título descritivo do gráfico
- Nomes dos eixos (com unidades)
- Legendas com símbolos e cores
- Notas rodapé (datas, fontes de dados)

Estilos:
- Cores consistentes (tema escuro/claro)
- Fontes legíveis
- Grid para facilitar leitura
- Proporções adequadas (aspect ratio)

Exportação:
- PNG/JPG: Qualidade alta para apresentações
- PDF: Relatórios profissionais
- SVG: Gráficos vetoriais escaláveis
- HTML: Gráficos interativos (plotly, bokeh)
- CSV: Dados tabulares para posterior análise

FLUXO DE GERAÇÃO DE GRÁFICOS:

┌────────────────────────────────────────┐
│ Dados de Resultado do Backtest         │
│ (histórico, trades, métricas)          │
└────────────────┬───────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   ┌────────────┐  ┌─────────────┐
   │ Processar  │  │ Processar   │
   │ Preços e   │  │ Trades e    │
   │ Indicadores│  │ Métricas    │
   └────────┬───┘  └──────┬──────┘
            │             │
            └────┬────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Criar Visualizações│
        │ (uma por tipo)     │
        └────────┬───────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   ┌────────────┐  ┌──────────────┐
   │ Aplicar    │  │ Organizar em │
   │ Formatação │  │ Layout Final │
   └────────┬───┘  └───────┬──────┘
            │              │
            └──────┬───────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Salvar em Múltiplos │
        │ Formatos (PNG, PDF) │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Gráficos Finalizados│
        │ Prontos para Uso    │
        └─────────────────────┘

MÉTRICAS EXIBIDAS:

Métricas Principais:
- Retorno Total (%): (Final - Inicial) / Inicial × 100
- Retorno Anualizado (%): Média de retorno por ano
- Volatilidade (Desvio Padrão): Risco medido por variação
- Sharpe Ratio: Retorno ajustado por risco
- Sortino Ratio: Sharpe mas penalizando apenas quedas

Métricas de Drawdown:
- Drawdown Máximo: Maior queda do pico
- Drawdown Médio: Média das quedas
- Duração do Drawdown: Tempo até recuperação

Métricas de Trades:
- Total de Trades: Quantidade de operações
- Taxa de Ganho: % de trades vencedores
- Fator de Lucro: Lucro total / Perda total
- Lucro Médio: Lucro por trade
- Razão Risk/Reward: Perda máxima / Ganho máximo

Performance:
- Dias com Ganho: Quantidade de dias positivos
- Win Streak: Maior sequência de ganhos
- Loss Streak: Maior sequência de perdas

ESTRUTURA DE EXPORTAÇÃO:

Diretório de Output:
```
./results/
├── charts/
│   ├── equity_curve.png
│   ├── drawdown.png
│   ├── price_chart.png
│   ├── indicators.png
│   ├── returns_distribution.png
│   └── trade_log.png
├── reports/
│   ├── summary_report.pdf
│   └── detailed_report.html
└── data/
    ├── trade_log.csv
    ├── daily_returns.csv
    └── metrics.json
```

DEPENDÊNCIAS:
- matplotlib: Gráficos estáticos
- plotly: Gráficos interativos
- seaborn: Estilos e análises estatísticas
- pandas: Manipulação e exportação de dados
- numpy: Operações numéricas
- fpdf/reportlab: Geração de PDF
- pillow: Processamento de imagens

CONFIGURAÇÕES CUSTOMIZÁVEIS:

Theme:
- 'dark': Tema escuro (padrão)
- 'light': Tema claro
- 'seaborn': Estilo seaborn

Resoluções:
- 'low': 72 DPI (web)
- 'medium': 150 DPI (padrão)
- 'high': 300 DPI (impressão profissional)

Formatos:
- Lista de formatos desejados
- Ex: ['png', 'pdf', 'html']

Idioma:
- 'pt': Português
- 'en': Inglês

EXEMPLO DE USO:
    from graphing.graphing import (
        plot_equity_curve,
        plot_trades,
        generate_report
    )
    
    # Gerar gráficos individuais
    plot_equity_curve(backtest_data, save_path='./results/')
    plot_trades(trade_history, save_path='./results/')
    
    # Gerar relatório completo
    generate_report(
        backtest_results,
        output_format=['png', 'pdf'],
        theme='dark',
        resolution='high'
    )

NOTAS:
- Gráficos devem ser formatados profissionalmente
- Suportar customização via parâmetros
- Exportar em múltiplos formatos para diferentes públicos
- Manter consistência de estilos entre gráficos
- Incluir informações essenciais (data, fonte de dados)
"""

import functools
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Tuple, Union

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
if __name__ == '__main__':
   # teste de sanidade
    series = generate_sample_time_series(length=30)
    plot_time_series(series, label='Série de Preço', colors=['#d62728'], line_style='-', marker='o')
    plt.show()