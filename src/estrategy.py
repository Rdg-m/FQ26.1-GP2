"""
Módulo de Implementação da Estratégia de Negociação

RESPONSABILIDADES:
- Definir as regras de entrada de posições (sinais de compra)
- Definir as regras de saída de posições (sinais de venda)
- Implementar cálculo de indicadores técnicos
- Gerar sinais de negociação para serem executados
- Ser flexível para permitir múltiplas estratégias
- Ser fácil de parametrizar e customizar

COMPONENTES PRINCIPAIS:

1. INDICADORES TÉCNICOS
   
   Indicadores de Tendência:
   - Simple Moving Average (SMA): Média aritmética simples
   - Exponential Moving Average (EMA): Média ponderada exponencial
   - MACD: Moving Average Convergence Divergence
   - ADX: Average Directional Index (força da tendência)
   
   Indicadores de Momentum:
   - RSI: Relative Strength Index (sobrecompra/sobrevenda)
   - Stochastic Oscillator: Posição do preço em range
   - Rate of Change (ROC): Taxa de mudança de preço
   - Momentum: Diferença de preço em n períodos
   
   Indicadores de Volatilidade:
   - Bollinger Bands: Bandas de desvio padrão
   - ATR: Average True Range (amplitude média)
   - Historical Volatility: Desvio padrão de retornos
   
   Indicadores de Volume:
   - On-Balance Volume (OBV): Volume acumulado
   - Volume Rate of Change: Taxa de mudança de volume
   - Money Flow Index (MFI): RSI ponderado por volume

2. REGRAS DE ENTRADA (SINAIS DE COMPRA)

   Exemplos de Regras:
   - Cruzamento de MAs: EMA rápida cruza acima de SMA lenta
   - MACD Positivo: MACD cruza acima da linha de sinal
   - RSI em Sobrevenda: RSI < 30
   - Toque em Suporte: Preço toca média móvel e rebota
   - Combinações: Múltiplas condições AND/OR
   
   Validação de Entrada:
   - Verificar capital disponível
   - Validar risco máximo por trade
   - Confirmar sinais antes de executar
   - Registrar motivo da entrada

3. REGRAS DE SAÍDA (SINAIS DE VENDA)

   Exemplos de Regras:
   - Stop Loss: Perda máxima definida (ex: 2% do capital)
   - Take Profit: Alvo de lucro (ex: 5% de ganho)
   - Cruzamento Oposto: Contrário do sinal de entrada
   - RSI em Sobrecompra: RSI > 70
   - Trailing Stop: Stop que sobe com o preço
   - Time-based: Sair após X dias/periodos
   
   Validação de Saída:
   - Confirmar que existe posição aberta
   - Validar valor de venda
   - Registrar motivo da saída
   - Calcular P&L da operação

4. PARÂMETROS DA ESTRATÉGIA

   Parâmetros de Indicadores:
   - Períodos de MAs: SMA 20, EMA 50, etc.
   - Thresholds de RSI: Sobrevenda 30, Sobrecompra 70
   - Períodos MACD: Fast 12, Slow 26, Signal 9
   
   Parâmetros de Risco:
   - Stop Loss em %: 2% do capital por trade
   - Take Profit em %: 5% a 10% por trade
   - Tamanho da posição: % do capital por trade
   - Máximo de posições abertas: 1, 2, 5 simultâneas
   
   Parâmetros Gerais:
   - Capital inicial: Quanto começar
   - Alavancagem: Multiplicador de posição (se permitido)
   - Comissões e Slippage: Custos de execução

FLUXO DE EXECUÇÃO:

┌──────────────────────────────┐
│ Preços Históricos do Ativo   │
│ (OHLCV - Open, High, Low...) │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│ Calcular Indicadores         │
│ (SMA, EMA, RSI, MACD, etc)   │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│ Avaliar Condições            │
│ (Regras de Entrada/Saída)    │
└────────────┬─────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
   COMPRA?      VENDA?
      │             │
      ▼             ▼
   Gerar      Gerar
   Sinal      Sinal
   Compra     Venda
      │             │
      └──────┬──────┘
             │
             ▼
┌──────────────────────────────┐
│ Retornar Sinais de Negócio   │
│ para backtesting_main.py     │
└──────────────────────────────┘

ESTRUTURA DO SINAL:

```python
{
    'timestamp': datetime,
    'symbol': 'AAPL',
    'signal_type': 'BUY' | 'SELL',
    'price': 150.25,
    'quantity': 100,
    'stop_loss': 147.25,
    'take_profit': 157.75,
    'reason': 'EMA fast crossed above EMA slow',
    'confidence': 0.85,  # 0-1 score
    'indicators': {
        'sma_20': 150.10,
        'ema_50': 149.85,
        'rsi': 45.2,
        'macd': 2.15,
        'atr': 2.50
    }
}
```

EXEMPLO DE ESTRATÉGIA SIMPLES:

    def simple_moving_average_crossover(prices, fast_period=20, slow_period=50):
        '''
        Estratégia: Cruzamento de Médias Móveis
        - Compra: EMA rápida cruza acima de SMA lenta
        - Venda: EMA rápida cruza abaixo de SMA lenta
        '''
        signals = []
        
        for i in range(max(fast_period, slow_period), len(prices)):
            fast_ma = prices[i-fast_period:i].mean()
            slow_ma = prices[i-slow_period:i].mean()
            prev_fast = prices[i-fast_period-1:i-1].mean()
            prev_slow = prices[i-slow_period-1:i-1].mean()
            
            # Sinal de compra
            if prev_fast <= prev_slow and fast_ma > slow_ma:
                signals.append({
                    'type': 'BUY',
                    'price': prices[i],
                    'reason': 'Fast MA crossed above Slow MA'
                })
            
            # Sinal de venda
            elif prev_fast >= prev_slow and fast_ma < slow_ma:
                signals.append({
                    'type': 'SELL',
                    'price': prices[i],
                    'reason': 'Fast MA crossed below Slow MA'
                })
        
        return signals

DEPENDÊNCIAS:
- pandas: Manipulação de dados de preços
- numpy: Operações numéricas
- talib: Indicadores técnicos (opcional, mais rápido)
- Bibliotecas customizadas para indicadores

CARACTERÍSTICAS:
- Flexível para implementar estratégias customizadas
- Parametrizável (fácil mudar valores)
- Suporta múltiplas estratégias simultâneas
- Gera sinais claros e auditáveis
- Inclui confidence score para cada sinal

NOTAS:
- Estratégia deve ser agnóstica a tipos de ativos
- Funciona com qualquer timeframe (1min a semanal)
- Não deve acessar dados futuros (look-ahead bias)
- Todos os cálculos devem ser determinísticos
- Deve ser testável e auditável
"""
