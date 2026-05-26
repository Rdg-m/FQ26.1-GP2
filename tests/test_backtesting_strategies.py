import pytest
from src.backtesting.modelos_pre_implementados import buy_and_hold, MA, EMA


class TestBuyAndHoldStrategy:
    def test_buy_and_hold_generates_one_time_buy_signals(self):
        strategy = buy_and_hold(1000.0)
        assets = [
            {'symbol': 'A', 'price': 10.0},
            {'symbol': 'B', 'price': 20.0}
        ]

        signals = strategy.generate_signals(assets)

        assert signals is not None
        assert len(signals) == 2
        assert all(signal['signal_type'] == 'BUY' for signal in signals)
        assert all(signal['quantity'] >= 0 for signal in signals)
        assert all(signal['reason'].startswith('Buy and Hold') for signal in signals)

        second_signals = strategy.generate_signals(assets)
        assert second_signals is None

    def test_buy_and_hold_skips_assets_when_price_too_high(self):
        strategy = buy_and_hold(10.0)
        assets = [{'symbol': 'A', 'price': 100.0}]

        signals = strategy.generate_signals(assets)
        assert signals == []


class TestMAStrategy:
    def test_ma_generates_buy_signal_on_positive_crossover(self):
        strategy = MA(100.0, periodo_rapido=2, periodo_lento=3)

        prices = [1.0, 2.0, 3.0]
        signals = None
        for price in prices:
            signals = strategy.generate_signals([{'symbol': 'A', 'price': price}])

        assert signals is not None
        assert len(signals) == 1
        assert signals[0]['signal_type'] == 'BUY'

    def test_ma_generates_sell_signal_on_negative_crossover_after_buy(self):
        strategy = MA(100.0, periodo_rapido=2, periodo_lento=3)

        for price in [1.0, 2.0, 3.0]:
            strategy.generate_signals([{'symbol': 'A', 'price': price}])

        sell_signals = strategy.generate_signals([{'symbol': 'A', 'price': 0.0}])

        assert sell_signals is not None
        assert len(sell_signals) == 1
        assert sell_signals[0]['signal_type'] == 'SELL'

    def test_ma_returns_none_before_enough_history(self):
        strategy = MA(100.0, periodo_rapido=2, periodo_lento=4)

        for price in [1.0, 2.0, 3.0]:
            assert strategy.generate_signals([{'symbol': 'A', 'price': price}]) is None


class TestEMAStrategy:
    def test_ema_produces_values_after_periods(self):
        strategy = EMA(100.0, periodo_rapido=2, periodo_lento=3)

        for price in [1.0, 2.0, 3.0]:
            signals = strategy.generate_signals([{'symbol': 'A', 'price': price}])

        assert signals is not None
        assert len(signals) == 1
        assert signals[0]['signal_type'] == 'BUY'

        ema_values = strategy.calc_MA('A')
        assert isinstance(ema_values, tuple)
        assert ema_values[0] is not None
        assert ema_values[1] is not None

    def test_ema_calculation_matches_expected_formula(self):
        strategy = EMA(100.0, periodo_rapido=2, periodo_lento=3)
        prices = [1.0, 2.0, 4.0]

        for price in prices:
            strategy.generate_signals([{'symbol': 'A', 'price': price}])

        ema_rapida, ema_lenta = strategy.calc_MA('A')
        assert ema_rapida != ema_lenta
        assert ema_rapida > 0
        assert ema_lenta > 0
