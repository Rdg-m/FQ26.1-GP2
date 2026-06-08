import pandas as pd
import numpy as np
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
        'signal': signal_line,
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