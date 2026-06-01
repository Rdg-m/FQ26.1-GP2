import pandas as pd
import numpy as np
import random as rd
from datetime import timedelta

from dataprocessing.mov_brow import MBG

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
        self.data_inicial =  pd.Timestamp('2024-01-01')
        self.data_atual =  self.data_inicial

        self.initial_capital=initial_capital
        self.cash=initial_capital
        self.portfolio_value=initial_capital
        self._configs = _config.copy()
        self.open_positions={}
        self.closed_positions=[] ##lista de dicionarios
        self.daily_history=[]    ##saldo de cada dia para fazermos os graficos


    def run(self,strategy_instance):
        if self._configs["dado_real"] == True: self._run_normal(strategy_instance)
        else: self._run_brown(strategy_instance)

    def _fluxo_padrao(self, ohlcv, strategy_instance):
        # Gerar sinais da estratégia
        # Processar sinais
        sinais = strategy_instance.generate_signals(ohlcv)
        if sinais: self._processar_sinal(sinais)
        
        # Verificar Stop Loss e Take Profit
        vendas_forcadas = self._verificar_stop_take(ohlcv)
        for sinal in vendas_forcadas:
            self._execute_sell(sinal)
        
        # Atualizar valor do portfolio
        self._atualizar_valor_protifolio(ohlcv)

    def _run_brown(self, strategy_instance):
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
        
    
        for _ in range(num_periodos):
            # Atualizar preços usando movimento browniano
            precos_atuais = {}
            for symbol in self.symbols:
                fator_multiplo = Step()
                precos_base[symbol] = max(0, precos_base[symbol] * fator_multiplo)
                precos_atuais[symbol] = precos_base[symbol]
            
            # Criar DataFrame OHLCV fictício para este período
            # com variação intra-período realista
            ohlcv = self._criar_ohlcv(precos_atuais)
            
            self._fluxo_padrao(ohlcv, strategy_instance)
            
            # Avançar para o próximo período
            self.data_atual += self._time_delta(1)
        
        print('back_finalizado (modo Browniano)')

    def _processar_sinal(self, sinais):
        for sinal in sinais:
            tipo = sinal["signal_type"]
            simbolo = sinal["symbol"]
            
            if tipo == "BUY":
                self._execute_buy(sinal)
            elif tipo == "SELL":
                if simbolo in self.open_positions:
                    self._execute_sell(sinal)
                else: raise AttributeError('simbolo não está nas posições abertas', simbolo)
            else: raise ValueError('Tipo de sinal mal formado', tipo)

    def _verificar_stop_take(self, ohlcv):
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
        return vendas_forcadas
            
    def _time_delta(self, n:int):
        match self._configs.get('time_period', 'd'):
            case 'd': return timedelta(days=n)
            case 'y': return timedelta(days=n*365)
            case 'M': return timedelta(days=n*30)
            case 'm': return timedelta(minutes=n)
            case _: raise ValueError('deixe configurado um horizonte correto')
    
    def _criar_ohlcv(self, precos_atuais):
        ohlcv_data = []
        for symbol in self.symbols:
            if self._configs['dado_real'] == False:
                preco_close = precos_atuais[symbol]
                preco_open = preco_close * (1 + rd.gauss(0, 0.005))
                preco_high = max(preco_open, preco_close) * (1 + abs(rd.gauss(0, 0.01)))
                preco_low = min(preco_open, preco_close) * (1 - abs(rd.gauss(0, 0.01)))
                volume = int(1000000 * (1 + rd.gauss(0, 0.2)))
            else: raise NotImplementedError('essa função só esta no back ficticio')

            ohlcv_data.append({
                'symbol': symbol,
                'open': preco_open,
                'high': preco_high,
                'low': preco_low,
                'close': preco_close,
                'volume': volume
            })
        
        return pd.DataFrame(ohlcv_data)

    def _atualizar_valor_protifolio(self, ohlcv):
        valor_acoes = 0
        for simbolo, posicao in self.open_positions.items():
            dados_da_acao = ohlcv[ohlcv['symbol'] == simbolo]
            
            if not dados_da_acao.empty:
                preco_fechamento = dados_da_acao['close'].iloc[0]
                posicao['value'] = posicao['quantity'] * preco_fechamento
            
            valor_acoes += posicao['value']
        
        self.portfolio_value = self.cash + valor_acoes
        
        self.daily_history.append({
            'date': self.data_atual,
            'cash': self.cash,
            'portfolio_value': self.portfolio_value
        })

    def _run_normal(self, strategy_instance):
        self.data=self.data.sort_index()            # Trocar por carregamento up-to-demand, sem processar tudo antes -rod
        datas_unicas=self.data.index.unique()       # achar outro método de saber iterações (imagino que um _config serve) -rod
        print('iniciado_o_back')
        for date in datas_unicas:
            ohlcv=self.data.loc[self.data.index==date]

            self._fluxo_padrao(ohlcv, strategy_instance)

        print('back_finalizado')

    def _overspending(self, sinal)-> tuple[float, int|float]:
        n=sinal['quantity']
        price_corr =sinal["price"] * (1+self.commission)
        while self.cash<price_corr*n:
            n -=1
        return price_corr*n, n
            
    def _execute_buy(self,sinal):
        custo=sinal["price"]*sinal["quantity"]* (1+self.commission)
        
        if self.cash < custo: 
            if self._configs['over_spend'] == False:
                print('sinal impossível (compra)'); return None                     #trazendo a chekagem pra dentro
            else:
                custo, sinal["quantity"] = self._overspending(sinal)                 # isso talvez a gente tira depois, pq isso significa que temos que informar o modelo de quanto dinheiro ele tem.
        
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
            self.open_positions[sinal["symbol"]]["date"]= self.data_atual
            self.open_positions[sinal["symbol"]]["stop_loss"] = sinal.get("stop_loss", 0.0)
            self.open_positions[sinal["symbol"]]["take_profit"] = sinal.get("take_profit", 0.0)
        else:
            self.open_positions[sinal["symbol"]] = {
                'symbol': sinal["symbol"],
                'quantity': sinal["quantity"],
                'entry_price': sinal["price"],
                'entry_date': self.data_atual,
                'stop_loss': sinal.get("stop_loss", 0.0),
                'take_profit': sinal.get("take_profit", 0.0),
                'entry_reason': sinal.get("reason", "N/A"),
                'value': sinal["price"] * sinal["quantity"]
            }

    def _execute_sell(self, sinal):
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
            'exit_date': self.data_atual,
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
    # fazendo vários exemplos para ficar mais ilustrado como usar o módulo talvez
    # só criar essa f pra ficar menos código em baixo:
    def print_resultados(engine):
        print('\nRESULTADOS DO BACKTEST')
        print('Cash final:', f'R$ {engine.cash:.2f}')
        print('Portfolio value final:', f'R$ {engine.portfolio_value:.2f}')
        print('Posições abertas:', engine.open_positions)
        print('Trades fechados:', len(engine.closed_positions))
        print('Dias simulados:', len(engine.daily_history))

    from .modelos_pre_implementados import buy_and_hold
    initial_capital =10000.0
    symbols = ['PETR4', 'VALE5', 'ITUB4']
    _config['dado_real'] = False
    _config['periodos'] = 15
    engine = BacktestEngine(pd.DataFrame(), symbols, initial_capital)


    print('Executando backtest browniano com estratégia buy_and_hold...')
    strategy = buy_and_hold(initial_capital)
    engine.run(strategy)

    print_resultados(engine)
    del engine

    from .modelos_pre_implementados import MA

    _config['periodos'] = 150
    engine = BacktestEngine(pd.DataFrame(), symbols, initial_capital)
    

    print('Executando backtest browniano com estratégia MA...')
    strategy = MA(initial_capital)
    engine.run(strategy)

    print_resultados(engine)
    del engine

    from .modelos_pre_implementados import EMA


    engine = BacktestEngine(pd.DataFrame(), symbols, initial_capital)


    print('Executando backtest browniano com estratégia EMA...')
    strategy = EMA(initial_capital)
    engine.run(strategy)

    print_resultados(engine)
    del engine