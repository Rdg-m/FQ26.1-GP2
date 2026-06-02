"""Backtesting strategy utilities.

This module exists as the preferred public strategy module name for the
`backtesting` package. It re-exports the indicator and signal utility functions
from `backtesting.estrategy` to preserve compatibility while providing a more
natural module name.
"""

from .estrategy import (
    adx,
    sma,
    ema,
    macd,
    rsi,
    stochastic,
    roc,
    momentum,
    bollinger_bands,
    atr,
    obv,
    volume_roc,
    mfi,
)

__all__ = [
    "adx",
    "sma",
    "ema",
    "macd",
    "rsi",
    "stochastic",
    "roc",
    "momentum",
    "bollinger_bands",
    "atr",
    "obv",
    "volume_roc",
    "mfi",
]
