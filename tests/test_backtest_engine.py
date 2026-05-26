import pandas as pd
from datetime import datetime
from src.backtesting import BacktestEngine


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

        engine._execute_buy(buy_signal, datetime.fromisoformat('2024-01-01'))
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

        engine._execute_sell(sell_signal, datetime.fromisoformat('2024-01-02'))
        assert engine.cash == 1010.0
        assert engine.open_positions == {}
        assert len(engine.closed_positions) == 1
        assert engine.closed_positions[0]['net_profit'] == 10.0

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
