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

#INDICADORES DE TENDÊNCIA

def adx(high, low, close, period=14):
    """
    Cálculo do Average Directional Index (ADX)
    - Mede a força da tendência
    - Valores acima de 25 indicam tendência forte
    - Valores abaixo de 20 indicam mercado lateral
    """
    # Implementação do cálculo do ADX
    plus_dm = high.diff()
    minus_dm = low.diff() * -1

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()

    plus_di = 100 * (plus_dm.rolling(window=period).sum() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).sum() / atr)

    dx = (
        (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    ) * 100

    adx = dx.rolling(window=period).mean()

    return adx

def sma(close: pd.Series, period: int = 20) -> pd.Series:
    """
    Cálculo da Simple Moving Average (SMA)
    - Média aritmética dos preços de fechamento
    - Usada para identificar tendências
    """
    return close.rolling(window=period).mean()

def ema(close: pd.Series, period: int = 20) -> pd.Series:
    """
    Cálculo da Exponential Moving Average (EMA)
    - Média ponderada que dá mais peso aos preços recentes
    - Reage mais rapidamente a mudanças de preço
    """
    return close.ewm(span=period, adjust=False).mean()

def macd(
        close: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
):
    """
    Cálculo do MACD (Moving Average Convergence Divergence)
    - Indicador de momentum e tendência
    - Linha MACD: EMA rápida - EMA lenta
    - Linha de sinal: EMA da linha MACD
    - Sinal de compra: MACD cruza acima da linha de sinal
    - Sinal de venda: MACD cruza abaixo da linha de sinal
    """
    ema_fast = ema(close, period=fast)
    ema_slow = ema(close, period=slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, period=signal)
    
    histogram = macd_line - signal_line
    
    return pd.DataFrame({
        'macd': macd_line,
        'signal': signal_line
        'histogram': histogram
    })

# INDICADORES DE MOMENTUM

def rsi(close: pd.Series, period: int = 14):

    """
    Cálculo do RSI (Relative Strength Index)
    - Mede a velocidade e mudança dos movimentos de preço
    - Valores acima de 70 indicam sobrecompra
    - Valores abaixo de 30 indicam sobrevenda
    """
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def stochastic(high, low, close, period=14):
    """
    Cálculo do Stochastic Oscillator
    - Mede a posição do preço de fechamento em relação ao range de preços
    - Valores acima de 80 indicam sobrecompra
    - Valores abaixo de 20 indicam sobrevenda
    """
    lowest_low = low.rolling(window=period).min()
    highest_high = high.rolling(window=period).max()

    k = (
        (close - lowest_low) / (highest_high - lowest_low)
    ) * 100

    d = k.rolling(window=3).mean()

    return pd.DataFrame({
        '%K': k,
        '%D': d
    })

def roc(close, period=12):

    return (
        (close - close.shift(period))
        / close.shift(period)
    ) * 100

def momentum(close, period=10):

    return close - close.shift(period)

# INDICADORES DE VOLATILIDADE

def bollinger_bands(close, period=20, std_mult=2):

    middle = sma(close, period)

    std = close.rolling(period).std()

    upper = middle + (std * std_mult)
    lower = middle - (std * std_mult)

    return pd.DataFrame({
        'upper': upper,
        'middle': middle,
        'lower': lower
    })

def atr(high, low, close, period=14):

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    return tr.rolling(period).mean()

def atr(high, low, close, period=14):

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    return tr.rolling(period).mean()

# INDICADORES DE VOLUME

def obv(close, volume):

    direction = np.sign(close.diff()).fillna(0)

    return (direction * volume).cumsum()

def volume_roc(volume, period=14):

    return (
        (volume - volume.shift(period))
        / volume.shift(period)
    ) * 100

def mfi(high, low, close, volume, period=14):

    typical_price = (high + low + close) / 3

    money_flow = typical_price * volume

    positive_flow = []
    negative_flow = []

    for i in range(1, len(typical_price)):

        if typical_price.iloc[i] > typical_price.iloc[i - 1]:
            positive_flow.append(money_flow.iloc[i])
            negative_flow.append(0)

        else:
            positive_flow.append(0)
            negative_flow.append(money_flow.iloc[i])

    positive_mf = pd.Series(positive_flow).rolling(period).sum()
    negative_mf = pd.Series(negative_flow).rolling(period).sum()

    mfr = positive_mf / negative_mf

    mfi = 100 - (100 / (1 + mfr))

    return mfi
