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
    from code.graphing.graphing import (
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
