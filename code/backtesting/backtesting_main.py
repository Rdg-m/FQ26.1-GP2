"""
Módulo Principal de Backtesting - Orquestração Completa do Sistema

RESPONSABILIDADES:
- Coordenar todo o processo de backtesting
- Gerenciar capital, portfolio e histórico de operações
- Executar sinais de compra e venda da estratégia
- Calcular métricas de desempenho
- Manter registro completo de transações
- Ser flexível para diferentes estratégias

FUNÇÃO PRINCIPAL:
Simular execução de uma estratégia de negociação em dados históricos,
registrando cada operação, atualização de capital, e calculando resultados.

FLUXO GERAL DE EXECUÇÃO:

┌─────────────────────────────────────────┐
│ 1. IMPORTAR BIBLIOTECAS E FUNÇÕES       │
│    (pandas, numpy, matplotlib, etc.)    │
│    (funções de load, clean, strategy)   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 2. CARREGAR DADOS HISTÓRICOS            │
│    (via load.py para múltiplos ativos)  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 3. PROCESSAR/LIMPAR DADOS               │
│    (via clean.py para validação)        │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 4. INICIALIZAR PARÂMETROS DO BACKTEST   │
│    - Capital inicial: valor inicial    │
│    - Período de tempo: data início/fim │
│    - Ativos a negociar: lista de símbolos
│    - Comissões: custo por transação    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 5. LOOP PRINCIPAL DO BACKTEST           │
│    Para cada período de tempo:          │
│    ┌─────────────────────────────────┐ │
│    │ a. Calcular indicadores         │ │
│    │ b. Gerar sinais (via strategy)  │ │
│    │ c. Executar ordens (BUY/SELL)   │ │
│    │ d. Atualizar capital/portfolio  │ │
│    │ e. Registrar histórico          │ │
│    └─────────────────────────────────┘ │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 6. CALCULAR MÉTRICAS FINAIS             │
│    - Retorno total e anualizado        │
│    - Volatilidade (Sharpe, Sortino)    │
│    - Drawdown máximo                   │
│    - Taxa de ganho                     │
│    - Fator de lucro                    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 7. VISUALIZAR RESULTADOS                │
│    (via graphing.py para gráficos)      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 8. RETORNAR RESULTADOS PARA INTERFACE   │
│    (para exibição ao usuário)           │
└─────────────────────────────────────────┘

VARIÁVEIS INICIAIS DO BACKTEST:

Capital e Portfolio:
- initial_capital: Capital com que começa (ex: R$ 10.000)
- current_capital: Capital disponível no momento
- total_portfolio_value: Valor total (capital + posições abertas)
- cash: Dinheiro em caixa

Período de Teste:
- start_date: Data de início do backtest
- end_date: Data de fim do backtest
- timeframe: Período dos dados (1m, 5m, 1h, 1d, 1w, 1M)

Ativos:
- symbols: Lista de ativos a negociar (ex: ['PETR4', 'VALE5'])
- data: Dataframe com dados históricos
- current_price: Preço atual de cada ativo

Custos:
- commission: Comissão por trade (ex: 0.1%)
- slippage: Diferença entre preço esperado e executado
- spread: Diferença bid/ask

Posições:
- open_positions: Dict de posições abertas
  {symbol: {'quantity': 100, 'entry_price': 50.25, 'entry_date': datetime}}
- closed_positions: Histórico de posições fechadas

ESTRUTURA DE DADOS - POSIÇÃO ABERTA:

```python
open_position = {
    'symbol': 'PETR4',
    'quantity': 100,            # Quantidade de ações
    'entry_price': 25.50,       # Preço de entrada
    'entry_date': datetime(...),
    'stop_loss': 24.95,         # Preço de parada
    'take_profit': 26.55,       # Alvo de lucro
    'entry_reason': 'EMA crossover',
    'value': 2550.00            # Valor total (qty × price)
}
```

ESTRUTURA DE DADOS - TRADE FECHADO:

```python
closed_trade = {
    'symbol': 'PETR4',
    'entry_date': datetime(...),
    'entry_price': 25.50,
    'entry_quantity': 100,
    'exit_date': datetime(...),
    'exit_price': 26.55,
    'exit_reason': 'Take profit',
    'gross_profit': 105.00,     # (26.55 - 25.50) × 100
    'commission': 5.10,         # Comissão de entrada + saída
    'net_profit': 99.90,        # Lucro líquido
    'return_percent': 4.12,     # (26.55 - 25.50) / 25.50 × 100
    'holding_days': 15
}
```

LOOP PRINCIPAL DETALHADO:

```python
for date in date_range(start_date, end_date):
    # Obter preços do dia
    ohlcv = get_price_data(date)
    
    # Calcular indicadores técnicos
    indicators = calculate_indicators(data_até_agora, ohlcv)
    
    # Gerar sinais da estratégia
    signals = estrategy.generate_signals(indicators, ohlcv)
    
    # Processar cada sinal
    for signal in signals:
        if signal['type'] == 'BUY':
            # Validar se há capital
            if current_capital >= signal['quantity'] * signal['price']:
                # Executar compra
                execute_buy(signal, ohlcv['close'], date)
                
        elif signal['type'] == 'SELL':
            # Validar se há posição aberta
            if has_open_position(signal['symbol']):
                # Executar venda
                execute_sell(signal, ohlcv['close'], date)
    
    # Avaliar posições abertas
    for position in open_positions.values():
        # Verificar stop loss
        if ohlcv['low'] <= position['stop_loss']:
            execute_sell_at_price(position, position['stop_loss'], date)
        
        # Verificar take profit
        elif ohlcv['high'] >= position['take_profit']:
            execute_sell_at_price(position, position['take_profit'], date)
    
    # Atualizar valor do portfolio
    portfolio_value = current_capital
    for position in open_positions.values():
        portfolio_value += position['quantity'] * ohlcv['close']
```

CÁLCULO DE MÉTRICAS:

Retorno:
- Total Return = (Final Value - Initial Value) / Initial Value
- Annual Return = (1 + Total Return) ^ (252 / trading_days) - 1
  (252 = dias de negociação por ano)

Volatilidade:
- Volatility = std(daily_returns)
- Annual Volatility = Volatility × sqrt(252)

Sharpe Ratio:
- Sharpe = (Annual Return - Risk Free Rate) / Annual Volatility
- Tipicamente Risk Free Rate = 3-5% ao ano

Sortino Ratio:
- Sortino = (Annual Return - Risk Free Rate) / Downside Deviation
- Downside Deviation = std(negative_returns_only)

Drawdown:
- Drawdown = (Current Value - Peak Value) / Peak Value
- Maximum Drawdown = maximum(all drawdowns)
- Calcula-se a série de máximos acumulados (peaks)

Win Rate:
- Win Rate = (Winning Trades / Total Trades) × 100
- Losing Trade = trade com net_profit < 0

Profit Factor:
- Profit Factor = Sum(Wins) / Sum(Losses)
- > 1.5 é considerado bom
- > 2.0 é excelente

DEPENDENCIES:
- pandas: Manipulação de dados
- numpy: Cálculos numéricos
- matplotlib/plotly: Visualização
- load.py: Carregamento de dados
- clean.py: Limpeza de dados
- estrategy.py: Sinais de negociação
- graphing.py: Gráficos de resultados

CONFIGURAÇÕES CUSTOMIZÁVEIS:
- Capital inicial
- Período de teste
- Estratégia a usar
- Parâmetros de comissão/slippage
- Tamanho máximo de posição
- Número máximo de posições abertas

EXEMPLO DE USO:
    from code.backtesting.backtesting_main import run_backtest
    
    results = run_backtest(
        symbols=['PETR4', 'VALE5'],
        start_date='2020-01-01',
        end_date='2023-12-31',
        initial_capital=10000,
        strategy='moving_average_crossover',
        commission=0.001
    )
    
    print(f"Total Return: {results['total_return']:.2%}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2%}")

NOTAS:
- Backtest é determinístico (mesmo resultado sempre)
- Não inclui riscos de execução real
- Assume liquidez suficiente
- Comissões e slippage são estimados
- Não simula impacto de grandes ordens
"""