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
    from src.backtesting.backtesting_main import run_backtest
    
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
import pandas as pd
import numpy as np
import random as rd
from datetime import datetime, timedelta
from typing import Callable
from src.dataprocessing.load import load_data
from src.dataprocessing.clean import clean_data
from src.dataprocessing.mov_brow import MBG
_config = {
    "over_spend": False,
    "mov_brown_parans": {'m' : 0.1, 'o' : .5}, #var diária tirada do cu
    "dado_real": True,
    "periodos" : 1000,
    "time_period": 'd' #ano y, dia d, mes M, minuto m


}

class BacktestEngine:
    def __init__(self,data:pd.DataFrame,symbols:list,initial_capital:float=10000.0,commission:float=0.001):
        self.data=data
        self.symbols=symbols
        self.commission=commission
        self.slipagge=0.0

        self.initial_capital=initial_capital
        self.cash=initial_capital
        self.portfolio_value=initial_capital
        self._configs = _config
        self.open_positions={}
        self.closed_positions=[] ##lista de dicionarios
        self.daily_history=[]    ##saldo de cada dia para fazermos os graficos


    def run(self,strategy_instance):
        if self._configs["dado_real"] == True: self.run_normal(strategy_instance)
        else: self.run_brown(strategy_instance)
        

    def run_brown(self, strategy_instance):
        """
        Executa backtest usando dados fictícios gerados com Movimento Browniano Geométrico.
        Usa os parâmetros em _configs para número de períodos, drift, volatilidade, etc.
        """
        print('iniciado_o_back (modo Browniano)')
        
        # Inicializar preços base para cada ativo
        precos_base = {symbol: 100.0 for symbol in self.symbols}
        
        # Obter parâmetros de configuração
        num_periodos = self._configs.get("periodos", 100)
        regime = self._configs.get("mov_brown_parans", {'m': 0, 'o': 50})

        # Obter funções de movimento browniano
        MOV, Step = MBG(regime['m'], regime['o'])
        
        # Data inicial
        data_atual = pd.Timestamp('2024-01-01')
    
        for periodo in range(num_periodos):
            # Atualizar preços usando movimento browniano
            precos_atuais = {}
            for symbol in self.symbols:
                fator_multiplo = Step()
                precos_base[symbol] = max(0, precos_base[symbol] * fator_multiplo)
                precos_atuais[symbol] = precos_base[symbol]
            
            # Criar DataFrame OHLCV fictício para este período
            # com variação intra-período realista
            ohlcv_data = []
            for symbol in self.symbols:
                preco_close = precos_atuais[symbol]
                preco_open = preco_close * (1 + rd.gauss(0, 0.005))
                preco_high = max(preco_open, preco_close) * (1 + abs(rd.gauss(0, 0.01)))
                preco_low = min(preco_open, preco_close) * (1 - abs(rd.gauss(0, 0.01)))
                volume = int(1000000 * (1 + rd.gauss(0, 0.2)))
                
                ohlcv_data.append({
                    'symbol': symbol,
                    'open': preco_open,
                    'high': preco_high,
                    'low': preco_low,
                    'close': preco_close,
                    'volume': volume
                })
            
            ohlcv = pd.DataFrame(ohlcv_data)
            
            # Gerar sinais da estratégia
            sinais = strategy_instance.generate_signals(ohlcv)
            
            # Processar sinais
            if sinais:
                for sinal in sinais:
                    tipo = sinal["signal_type"]
                    simbolo = sinal["symbol"]
                    
                    if tipo == "BUY":
                        self._execute_buy(sinal, data_atual)
                    elif tipo == "SELL":
                        if simbolo in self.open_positions:
                            self._execute_sell(sinal, data_atual)
            
            # Verificar Stop Loss e Take Profit
            vendas_forcadas = []
            for simbolo, posicao in list(self.open_positions.items()):
                dados_acao = ohlcv[ohlcv["symbol"] == simbolo]
                if dados_acao.empty:
                    continue
                
                minima = dados_acao["low"].iloc[0]
                maxima = dados_acao["high"].iloc[0]
                stop = posicao.get('stop_loss', 0.0)
                alvo = posicao.get('take_profit', 0.0)
                
                if stop > 0 and minima <= stop:
                    sinal_venda = {
                        "symbol": simbolo,
                        "price": stop,
                        "quantity": posicao['quantity'],
                        "reason": "Stop Loss Atingido"
                    }
                    vendas_forcadas.append(sinal_venda)
                elif alvo > 0 and maxima >= alvo:
                    sinal_venda = {
                        "symbol": simbolo,
                        "price": alvo,
                        "quantity": posicao['quantity'],
                        "reason": "Take Profit Atingido"
                    }
                    vendas_forcadas.append(sinal_venda)
            
            for sinal in vendas_forcadas:
                self._execute_sell(sinal, data_atual)
            
            # Atualizar valor do portfolio
            valor_acoes = 0
            for simbolo, posicao in self.open_positions.items():
                dados_da_acao = ohlcv[ohlcv['symbol'] == simbolo]
                
                if not dados_da_acao.empty:
                    preco_fechamento = dados_da_acao['close'].iloc[0]
                    posicao['value'] = posicao['quantity'] * preco_fechamento
                
                valor_acoes += posicao['value']
            
            self.portfolio_value = self.cash + valor_acoes
            
            self.daily_history.append({
                'date': data_atual,
                'cash': self.cash,
                'portfolio_value': self.portfolio_value
            })
            
            # Avançar para o próximo período
            data_atual += timedelta(days=1)
        
        print('back_finalizado (modo Browniano)')


    def run_normal(self, strategy_instance):
        self.data=self.data.sort_index()            # Trocar por carregamento up-to-demand, sem processar tudo antes -rod
        datas_unicas=self.data.index.unique()       # achar outro método de saber iterações (imagino que um _config serve) -rod
        print('iniciado_o_back')
        for date in datas_unicas:
            ohlcv=self.data.loc[self.data.index==date]
            sinais=strategy_instance.generate_signals(ohlcv)
            for sinal in sinais:
                tipo=sinal["signal_type"]
                simbolo=sinal["symbol"]
                preco=sinal["price"]
                qtd=sinal['quantity']
                # tempo=sinal["timestamp"]          # não está sendo usado -rod
                # stop_loss=sinal["stop_loss"]
                # take_profit=sinal["take_profit"]
                # reason=sinal.get("reason")
                # confidence=sinal.get("confidence")
                # indicators=sinal.get("indicators")
                if tipo=="BUY": self._execute_buy(sinal,date)
                    
                elif tipo=="SELL":
                    if simbolo in self.open_positions:
                        self._execute_sell(sinal,date)
                    else: raise AttributeError('simbolo não está nas posições abertas', simbolo)
                else: raise ValueError('Tipo de sinal mal formado', tipo)
                
            vendas_forcadas=[]
            for simbolo,posicao in self.open_positions.items():
                dados_acao=ohlcv[ohlcv["symbol"]==simbolo]
                if dados_acao.empty:
                    continue
                minima=dados_acao["low"].iloc[0]
                maxima=dados_acao["high"].iloc[0]
                stop = posicao.get('stop_loss', 0.0)
                alvo = posicao.get('take_profit', 0.0)
                if stop>0 and minima<= stop:
                    sinal_venda = {
                        "symbol": simbolo,
                        "price": stop, 
                        "quantity": posicao['quantity'], 
                        "reason": "Stop Loss Atingido"
                    }
                    vendas_forcadas.append(sinal_venda)
                elif alvo > 0 and maxima >= alvo:
                    sinal_venda = {
                        "symbol": simbolo,
                        "price": alvo,
                        "quantity": posicao['quantity'], 
                        "reason": "Take Profit Atingido"
                    }
                    vendas_forcadas.append(sinal_venda)
            
            for sinal in vendas_forcadas:
                self._execute_sell(sinal, date)
        
            #analise do dia
            valor_acoes = 0
            for simbolo, posicao in self.open_positions.items():
                dados_da_acao = ohlcv[ohlcv['symbol'] == simbolo]
                
                if not dados_da_acao.empty:
                    preco_fechamento = dados_da_acao['close'].iloc[0]
                    posicao['value'] = posicao['quantity'] * preco_fechamento       #atualiza -rod
                
                valor_acoes += posicao['value']                                     #fica fora do if, pois se faltar não atualiza saquei -rod
                
            self.portfolio_value = self.cash + valor_acoes
            
            self.daily_history.append({
                'date': date,
                'cash': self.cash,
                'portfolio_value': self.portfolio_value
            })
        print('back_finalizado')

    def overspending(self, sinal)-> tuple[float, int|float]:
        n=sinal['quantity']
        price_corr =sinal["price"] * (1+self.commission)
        while self.cash<price_corr*n:
            n -=1
        return price_corr*n, n
            

    def _execute_buy(self,sinal,date):
        custo=sinal["price"]*sinal["quantity"]* (1+self.commission)
        
        if self.cash < custo: 
            if self._configs['over_spend'] == False:
                print('sinal impossível (compra)'); return None                     #trazendo a chekagem pra dentro
            else:
                custo, sinal["quantity"] = self.overspending(sinal)                 # isso talvez a gente tira depois, pq isso significa que temos que informar o modelo de quanto dinheiro ele tem.
        
        self.cash=self.cash-custo
        if sinal["symbol"] in self.open_positions:
            qtd_antiga=self.open_positions[sinal["symbol"]]["quantity"]             #talvez precise usar get com exception como 0, para sempre funcionar -rod
            preco_antigo=self.open_positions[sinal["symbol"]]["entry_price"]        #mesma coisa -rod
            qtd_nova=sinal["quantity"]
            preco_novo=sinal["price"]
            qtd_total = qtd_antiga + qtd_nova
            valor_novo = (qtd_antiga * preco_antigo) + (qtd_nova * preco_novo)      #menos rounding -rod
            preco_medio = valor_novo / qtd_total
            self.open_positions[sinal["symbol"]]["quantity"] = qtd_total
            self.open_positions[sinal["symbol"]]["entry_price"] = preco_medio
            self.open_positions[sinal["symbol"]]["value"] = valor_novo
            self.open_positions[sinal["symbol"]]["date"]= date
            self.open_positions[sinal["symbol"]]["stop_loss"] = sinal.get("stop_loss", 0.0)
            self.open_positions[sinal["symbol"]]["take_profit"] = sinal.get("take_profit", 0.0)
        else:
            self.open_positions[sinal["symbol"]] = {
                'symbol': sinal["symbol"],
                'quantity': sinal["quantity"],
                'entry_price': sinal["price"],
                'entry_date': date,
                'stop_loss': sinal.get("stop_loss", 0.0),
                'take_profit': sinal.get("take_profit", 0.0),
                'entry_reason': sinal.get("reason", "N/A"),
                'value': sinal["price"] * sinal["quantity"]
            }


    def _execute_sell(self, sinal, date):
        simbolo = sinal["symbol"]
        preco_venda = sinal["price"]
        
        posicao = self.open_positions[simbolo]
        qtd_venda = min(sinal["quantity"], posicao["quantity"])
        preco_entrada = posicao["entry_price"]
        data_entrada = posicao["entry_date"]
        
        valor_bruto_venda = preco_venda * qtd_venda

        valor_liquido_venda = valor_bruto_venda *(1-self.commission)    #fiz a conta direta que parece mais claro -rod  
        
        self.cash = self.cash + valor_liquido_venda

        custo_da_venda = qtd_venda * preco_entrada                      
        lucro_liquido = valor_liquido_venda - custo_da_venda
        
        trade_fechado = {
            'symbol': simbolo,
            'entry_date': data_entrada,
            'entry_price': preco_entrada,
            'exit_date': date,
            'exit_price': preco_venda,
            'quantity': qtd_venda,
            'net_profit': lucro_liquido,
            'exit_reason': sinal.get("reason", "Sinal da Estratégia")
        }
        self.closed_positions.append(trade_fechado)
        
        posicao["quantity"] = posicao["quantity"] - qtd_venda
        posicao["value"] = posicao["quantity"] * preco_entrada
        if posicao["quantity"] <= 0:
            del self.open_positions[simbolo]


if __name__ == '__main__':
    from src.backtesting.modelos_pre_implementados import buy_and_hold
    initial_capital =10000.0
    symbols = ['PETR4', 'VALE5', 'ITUB4']
    _config['dado_real'] = False
    _config['periodos'] = 15
    engine = BacktestEngine(pd.DataFrame(), symbols, initial_capital)


    print('Executando backtest browniano com estratégia buy_and_hold...')
    strategy = buy_and_hold(initial_capital)
    engine.run(strategy)

    print('\nRESULTADOS DO BACKTEST')
    print('Cash final:', f'R$ {engine.cash:.2f}')
    print('Portfolio value final:', f'R$ {engine.portfolio_value:.2f}')
    print('Posições abertas:', engine.open_positions)
    print('Trades fechados:', len(engine.closed_positions))
    print('Dias simulados:', len(engine.daily_history))
  
    from src.backtesting.modelos_pre_implementados import MA

    _config['periodos'] = 150
    engine = BacktestEngine(pd.DataFrame(), symbols, initial_capital)
    

    print('Executando backtest browniano com estratégia buy_and_hold...')
    strategy = MA(initial_capital)
    engine.run(strategy)

    print('\nRESULTADOS DO BACKTEST')
    print('Cash final:', f'R$ {engine.cash:.2f}')
    print('Portfolio value final:', f'R$ {engine.portfolio_value:.2f}')
    print('Posições abertas:', engine.open_positions)
    print('Trades fechados:', len(engine.closed_positions))
    print('Dias simulados:', len(engine.daily_history))

    from src.backtesting.modelos_pre_implementados import EMA


    engine = BacktestEngine(pd.DataFrame(), symbols, initial_capital)


    print('Executando backtest browniano com estratégia buy_and_hold...')
    strategy = EMA(initial_capital)
    engine.run(strategy)

    print('\nRESULTADOS DO BACKTEST')
    print('Cash final:', f'R$ {engine.cash:.2f}')
    print('Portfolio value final:', f'R$ {engine.portfolio_value:.2f}')
    print('Posições abertas:', engine.open_positions)
    print('Trades fechados:', len(engine.closed_positions))
    print('Dias simulados:', len(engine.daily_history))