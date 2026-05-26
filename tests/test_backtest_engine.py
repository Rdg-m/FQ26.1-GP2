import pandas as pd
import pytest
from datetime import datetime, timedelta
from backtesting import BacktestEngine


class DummyStrategy:
    def __init__(self):
        self.calls = 0

    def generate_signals(self, ohlcv):
        self.calls += 1
        return None


class BuyFirstPeriodStrategy:
    def __init__(self):
        self.calls = 0

    def generate_signals(self, ohlcv):
        if self.calls == 0:
            self.calls += 1
            return [
                {
                    'signal_type': 'BUY',
                    'symbol': 'A',
                    'price': float(ohlcv['close'].iloc[0]),
                    'quantity': 1,
                    'reason': 'Compra inicial'
                }
            ]
        self.calls += 1
        return None


class TestBacktestEngine:
    def test_engine_initial_state(self):
        engine = BacktestEngine(pd.DataFrame(), ['A', 'B'], initial_capital=1000.0, commission=0.001)

        assert engine.cash == 1000.0
        assert engine.initial_capital == 1000.0
        assert engine.portfolio_value == 1000.0
        assert engine.open_positions == {}
        assert engine.closed_positions == []
        assert engine.daily_history == []

    def test_overspending_reduces_quantity(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=50.0, commission=0.1)
        signal = {
            'symbol': 'A',
            'price': 10.0,
            'quantity': 10
        }

        new_cost, new_quantity = engine._overspending(signal)

        assert new_quantity < 10
        assert new_cost == new_quantity * signal['price'] * (1 + engine.commission)
        assert new_quantity == 4

    def test_execute_buy_and_sell_updates_positions(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=1000.0, commission=0.0)
        buy_signal = {
            'symbol': 'A',
            'signal_type': 'BUY',
            'price': 10.0,
            'quantity': 10,
            'reason': 'Teste compra'
        }

        engine._execute_buy(buy_signal)
        assert engine.cash == 900.0
        assert 'A' in engine.open_positions
        assert engine.open_positions['A']['quantity'] == 10
        assert engine.open_positions['A']['entry_price'] == 10.0

        sell_signal = {
            'symbol': 'A',
            'signal_type': 'SELL',
            'price': 11.0,
            'quantity': 10,
            'reason': 'Teste venda'
        }

        engine._execute_sell(sell_signal)
        assert engine.cash == 1010.0
        assert engine.open_positions == {}
        assert len(engine.closed_positions) == 1
        assert engine.closed_positions[0]['net_profit'] == 10.0

    def test_execute_buy_aggregates_existing_position(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=2000.0, commission=0.0)

        engine._execute_buy({'symbol': 'A', 'signal_type': 'BUY', 'price': 10.0, 'quantity': 10})
        engine._execute_buy({'symbol': 'A', 'signal_type': 'BUY', 'price': 20.0, 'quantity': 5})

        assert engine.open_positions['A']['quantity'] == 15
        assert engine.open_positions['A']['entry_price'] == pytest.approx((10.0 * 10 + 20.0 * 5) / 15)
        assert engine.cash == 2000.0 - 10.0 * 10 - 20.0 * 5

    def test_execute_sell_partial_position(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=1000.0, commission=0.0)
        engine._execute_buy({'symbol': 'A', 'signal_type': 'BUY', 'price': 10.0, 'quantity': 10})

        engine._execute_sell({'symbol': 'A', 'price': 11.0, 'quantity': 4, 'reason': 'Partial sell'})

        assert engine.open_positions['A']['quantity'] == 6
        assert engine.cash == 944.0
        assert len(engine.closed_positions) == 1
        assert engine.closed_positions[0]['net_profit'] == 4.0

    def test_processar_sinal_rejects_invalid_signal_type(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=1000.0)

        with pytest.raises(ValueError):
            engine._processar_sinal([
                {'signal_type': 'HOLD', 'symbol': 'A', 'price': 10.0, 'quantity': 1}
            ])

    def test_processar_sinal_rejects_sell_without_open_position(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=1000.0)

        with pytest.raises(AttributeError):
            engine._processar_sinal([
                {'signal_type': 'SELL', 'symbol': 'A', 'price': 10.0, 'quantity': 1}
            ])

    def test_verificar_stop_take_generates_stop_loss(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=1000.0, commission=0.0)
        engine.open_positions['A'] = {
            'quantity': 10,
            'entry_price': 10.0,
            'stop_loss': 9.5,
            'take_profit': 11.5
        }

        ohlcv = pd.DataFrame([
            {'symbol': 'A', 'open': 10.0, 'high': 10.5, 'low': 9.0, 'close': 10.0, 'volume': 1000}
        ])

        sinais = engine._verificar_stop_take(ohlcv)
        assert len(sinais) == 1
        assert sinais[0]['reason'] == 'Stop Loss Atingido'

    def test_verificar_stop_take_generates_take_profit(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=1000.0, commission=0.0)
        engine.open_positions['A'] = {
            'quantity': 10,
            'entry_price': 10.0,
            'stop_loss': 9.0,
            'take_profit': 11.5
        }

        ohlcv = pd.DataFrame([
            {'symbol': 'A', 'open': 10.0, 'high': 12.0, 'low': 10.5, 'close': 11.5, 'volume': 1000}
        ])

        sinais = engine._verificar_stop_take(ohlcv)
        assert len(sinais) == 1
        assert sinais[0]['reason'] == 'Take Profit Atingido'

    def test_time_delta_supports_all_periods(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'])
        engine._configs['time_period'] = 'd'
        assert engine._time_delta(2) == timedelta(days=2)

        engine._configs['time_period'] = 'y'
        assert engine._time_delta(1) == timedelta(days=365)

        engine._configs['time_period'] = 'M'
        assert engine._time_delta(1) == timedelta(days=30)

        engine._configs['time_period'] = 'm'
        assert engine._time_delta(1) == timedelta(minutes=1)

        engine._configs['time_period'] = 'invalid'
        with pytest.raises(ValueError):
            engine._time_delta(1)

    def test_run_normal_populates_daily_history(self):
        dates = [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-02')]
        df = pd.DataFrame([
            {'symbol': 'A', 'open': 10.0, 'high': 10.5, 'low': 9.5, 'close': 10.0, 'volume': 1000, 'date': dates[0]},
            {'symbol': 'A', 'open': 10.2, 'high': 10.8, 'low': 10.1, 'close': 10.5, 'volume': 1000, 'date': dates[1]}
        ]).set_index('date')

        engine = BacktestEngine(df, ['A'], initial_capital=100.0, commission=0.0)
        engine._configs['dado_real'] = True
        engine.run(DummyStrategy())

        assert len(engine.daily_history) == 2
        assert engine.daily_history[0]['portfolio_value'] == 100.0
        assert engine.daily_history[1]['portfolio_value'] == 100.0

    def test_run_brown_with_no_signals_keeps_cash(self):
        engine = BacktestEngine(pd.DataFrame(), ['A', 'B'], initial_capital=500.0, commission=0.0)
        engine._configs['dado_real'] = False
        engine._configs['periodos'] = 5

        engine.run(DummyStrategy())

        assert engine.cash == 500.0
        assert engine.open_positions == {}
        assert engine.closed_positions == []
        assert len(engine.daily_history) == 5
        assert engine.portfolio_value == 500.0

    def test_run_brown_executes_first_buy_signal(self):
        engine = BacktestEngine(pd.DataFrame(), ['A'], initial_capital=100.0, commission=0.0)
        engine._configs['dado_real'] = False
        engine._configs['periodos'] = 3

        strategy = BuyFirstPeriodStrategy()
        engine.run(strategy)

        assert len(engine.daily_history) == 3
        assert engine.cash < 100.0
        assert engine.cash > 0.0
        assert 'A' in engine.open_positions
        assert engine.open_positions['A']['quantity'] == 1
        assert strategy.calls == 3
