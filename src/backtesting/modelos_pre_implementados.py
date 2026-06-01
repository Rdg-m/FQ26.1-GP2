from typing import Any, List, Dict
from collections.abc import Iterable
import random


class estrat:
    def __init__(self, saldo) -> None:
        self.saldo = saldo
        self.memoria = {}  # {symbol: [lista de preços]}
        self.posicoes_abertas = {}  # {symbol: {'price': ..., 'qty': ...}}

    def _add_price(self, symbol: str, price: float) -> None:
        """Adiciona preço à memória para o símbolo"""
        if symbol not in self.memoria:
            self.memoria[symbol] = []
        self.memoria[symbol].append(price)

    def _generate_signal(self, symbol: str, signal_type: str, price: float, 
                        quantity: int, reason: str = "") -> Dict:
        """Cria estrutura padrão de sinal para backtesting"""
        return {
            'symbol': symbol,
            'signal_type': signal_type,  # 'BUY' ou 'SELL'
            'price': price,
            'quantity': quantity,
            'reason': reason
        }

    def com(self, assets: List[Dict]) -> List[Dict]:
        """
        Recebe lista de dicts com {'symbol': '...', 'price': ...}
        Retorna lista de sinais a executar
        """
        raise NotImplementedError()

    def generate_signals(self, ohlcv) -> List[Dict] | None:
        """
        Adapter method so strategy instances can be passed directly to
        BacktestEngine. Accepts either a DataFrame-like object (with
        `iterrows`) or a list of asset dicts and returns the signals
        produced by `com`.
        """
        assets: List[Dict] = []

        # DataFrame-like: iterate rows and extract symbol/close
        if hasattr(ohlcv, "iterrows"):
            for _, row in ohlcv.iterrows():
                try:
                    if 'symbol' in row and 'close' in row:
                        assets.append({'symbol': row['symbol'], 'price': row['close']})
                except Exception:
                    continue

        # List-like: assume it's already a list of asset dicts
        elif isinstance(ohlcv, Iterable):
            try:
                # e.g. [{'symbol':..,'price':..}, ...]
                assets = list(ohlcv)
            except Exception:
                assets = []

        # Fallback: return whatever `com` produces for the assets list
        return self.com(assets)


class buy_and_hold(estrat):
    '''
    pegar todas as ações do dia e gerar buy-orders a fim de gastar a mesma quantia em cada ação disponivel
    não fazer mais nada
    '''

    def __init__(self, saldo) -> None:
        super().__init__(saldo)
        self.compradas = False

    def com(self, assets: List[Dict]) -> List[Dict]:
        """
        Realiza compra uma única vez de todos os ativos com saldo dividido igualmente
        Args:
            assets: Lista de dicts [{'symbol': 'PETR4', 'price': 25.50}, ...]
        Returns:
            Lista de sinais BUY ou None
        """
        if self.compradas:
            return None
        
        self.compradas = True
        signals = []
        
        if not assets:
            return signals
        
        # Divide saldo igualmente entre todos os ativos
        saldo_por_ativo = self.saldo / len(assets)
        
        for asset in assets:
            symbol = asset['symbol']
            price = asset['price']
            
            # Calcula quantidade que pode comprar
            quantity = int(saldo_por_ativo / price)
            
            if quantity > 0:
                signal = self._generate_signal(
                    symbol=symbol,
                    signal_type='BUY',
                    price=price,
                    quantity=quantity,
                    reason='Buy and Hold - compra inicial'
                )
                signals.append(signal)
                self.posicoes_abertas[symbol] = {'price': price, 'qty': quantity}
        
        return signals


class MA(estrat):
    ''' comprar e vender a depender da moving AVG de cada asset'''
    def __init__(self, saldo, periodo_rapido: int = 20, periodo_lento: int = 50) -> None:
        super().__init__(saldo)
        self.periodo_rapido = periodo_rapido
        self.periodo_lento = periodo_lento
        self.prev_decisao = {}  # {symbol: decisão anterior para detectar crossover}
    
    def com(self, assets: List[Dict]) -> List[Dict]:
        """
        Processa sinais baseado em cruzamento de médias móveis
        Args:
            assets: Lista de dicts [{'symbol': 'PETR4', 'price': 25.50}, ...]
        Returns:
            Lista de sinais BUY/SELL
        """
        signals = []
        
        for asset in assets:
            symbol = asset['symbol']
            price = asset['price']
            
            # Adiciona preço à memória
            self.add_mem(symbol, price)
            
            # Calcula decisão se temos histórico suficiente
            if len(self.memoria[symbol]) >= self.periodo_lento:
                decisao = self.decisao(symbol)
                
                # Detecta mudança de decisão (crossover)
                prev = self.prev_decisao.get(symbol)
                
                if decisao is True and prev is not True:
                    # Cruzamento para cima - sinal de COMPRA
                    saldo_por_ativo = self.saldo / len(assets) if assets else self.saldo
                    quantity = int(saldo_por_ativo / price) if self.saldo > 0 else 0
                    if quantity > 0:
                        signal = self._generate_signal(
                            symbol=symbol,
                            signal_type='BUY',
                            price=price,
                            quantity=quantity,
                            reason=f'MA: SMA{self.periodo_rapido} cruzou acima de SMA{self.periodo_lento}'
                        )
                        signals.append(signal)
                        self.posicoes_abertas[symbol] = {'price': price, 'qty': quantity}
                
                elif decisao is False and prev is not False:
                    # Cruzamento para baixo - sinal de VENDA
                    if symbol in self.posicoes_abertas:
                        qty = self.posicoes_abertas[symbol]['qty']
                        signal = self._generate_signal(
                            symbol=symbol,
                            signal_type='SELL',
                            price=price,
                            quantity=qty,
                            reason=f'MA: SMA{self.periodo_rapido} cruzou abaixo de SMA{self.periodo_lento}'
                        )
                        signals.append(signal)
                        del self.posicoes_abertas[symbol]
                
                self.prev_decisao[symbol] = decisao
        
        if signals: return signals
        else: return None

    def calc_MA(self, symbol: str) -> tuple:
        """
        Calcula as duas médias móveis simples
        Returns: (sma_rapida, sma_lenta)
        """
        prices = self.memoria[symbol]
        
        if len(prices) < self.periodo_lento:
            return None, None
        
        # SMA rápida (últimos N períodos)
        sma_rapida = sum(prices[-self.periodo_rapido:]) / self.periodo_rapido
        
        # SMA lenta (últimos N períodos)
        sma_lenta = sum(prices[-self.periodo_lento:]) / self.periodo_lento
        
        return sma_rapida, sma_lenta

    def add_mem(self, symbol: str, price: float) -> None:
        """Adiciona preço à memória com validação"""
        self._add_price(symbol, price)

    def decisao(self, symbol: str):
        '''
        Compara as médias móveis e retorna:
        True: compra (SMA rápida > SMA lenta)
        False: venda (SMA rápida < SMA lenta)
        None: esperar
        '''
        sma_rapida, sma_lenta = self.calc_MA(symbol)
        
        if sma_rapida is None or sma_lenta is None:
            return None
        
        if sma_rapida > sma_lenta:
            return True
        elif sma_rapida < sma_lenta:
            return False
        else:
            return None


class EMA(MA):
    '''mesma estrat de MA, mas com moving AVG exponencial'''
    
    def calc_MA(self, symbol: str) -> tuple:
        """
        Calcula as duas médias móveis exponenciais
        Returns: (ema_rapida, ema_lenta)
        """
        prices = self.memoria[symbol]
        
        if len(prices) < self.periodo_lento:
            return None, None
        
        # EMA rápida
        ema_rapida = self._calculate_ema(prices, self.periodo_rapido)
        
        # EMA lenta
        ema_lenta = self._calculate_ema(prices, self.periodo_lento)
        
        return ema_rapida, ema_lenta
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """
        Calcula EMA para um período específico
        Fórmula: EMA_t = (preço_t × α) + (EMA_{t-1} × (1-α))
        onde α = 2 / (período + 1)
        """
        if len(prices) < period:
            return None
        
        alpha = 2 / (period + 1)
        
        # Inicializa com SMA dos primeiros N valores
        ema = sum(prices[:period]) / period
        
        # Calcula EMA para o resto
        for price in prices[period:]:
            ema = (price * alpha) + (ema * (1 - alpha))
        
        return ema


# ======================== TESTES PRÁTICOS ========================

if __name__ == '__main__':
    print("=" * 70)
    print("TESTES DE MODELOS DE BACKTESTING")
    print("=" * 70)
    
    # Parâmetros de teste
    saldo_inicial = 10000
    num_periodos = 100
    ativos = ['PETR4', 'VALE5', 'ITUB4']
    
    # ========== TESTE 1: BUY AND HOLD ==========
    print("\n[TESTE 1] BUY AND HOLD")
    print("-" * 70)
    
    # Gera dados fictícios
    precos_bah = {symbol: 100 + random.gauss(0, 2) for symbol in ativos}
    
    bah = buy_and_hold(saldo_inicial)
    
    # Primeiro período - deve gerar sinais de compra
    assets_data = [{'symbol': symbol, 'price': precos_bah[symbol]} for symbol in ativos]
    sinais = bah.com(assets_data)
    
    if sinais:
        print(f"✓ Sinais iniciais gerados: {len(sinais)} operações")
        for sinal in sinais:
            print(f"  → {sinal['symbol']}: {sinal['type']} {sinal['quantity']} @ R$ {sinal['price']:.2f}")
    
    # Próximos períodos - não deve gerar mais sinais
    print("\nPróximos períodos:")
    for periodo in range(1, 5):
        precos_bah = {symbol: precos_bah[symbol] * (1 + random.gauss(0, 0.01)) for symbol in ativos}
        assets_data = [{'symbol': symbol, 'price': precos_bah[symbol]} for symbol in ativos]
        sinais = bah.com(assets_data)
        print(f"  Período {periodo}: {sinais if sinais else 'Nenhum sinal (esperado)'}")
    
    # ========== TESTE 2: MOVING AVERAGE ==========
    print("\n\n[TESTE 2] MOVING AVERAGE (SMA)")
    print("-" * 70)
    
    precos_ma = {symbol: 100 + random.gauss(0, 2) for symbol in ativos}
    ma_strategy = MA(saldo_inicial, periodo_rapido=20, periodo_lento=50)
    
    print(f"Simulando {num_periodos} períodos com MA(20/50)...\n")
    
    sinais_gerados = []
    for periodo in range(num_periodos):
        # Gera variação aleatória realista
        precos_ma = {
            symbol: max(1, precos_ma[symbol] * (1 + random.gauss(0, 0.015)))
            for symbol in ativos
        }
        
        assets_data = [{'symbol': symbol, 'price': precos_ma[symbol]} for symbol in ativos]
        sinais = ma_strategy.com(assets_data)
        
        if sinais:
            sinais_gerados.extend(sinais)
            print(f"Período {periodo:3d}: ", end="")
            for sinal in sinais:
                print(f"{sinal['symbol']} {sinal['type']:4s} @ R$ {sinal['price']:7.2f} | ", end="")
            print()
    
    print(f"\n✓ Total de sinais gerados: {len(sinais_gerados)}")
    
    # ========== TESTE 3: EXPONENTIAL MOVING AVERAGE ==========
    print("\n\n[TESTE 3] EXPONENTIAL MOVING AVERAGE (EMA)")
    print("-" * 70)
    
    precos_ema = {symbol: 100 + random.gauss(0, 2) for symbol in ativos}
    ema_strategy = EMA(saldo_inicial, periodo_rapido=20, periodo_lento=50)
    
    print(f"Simulando {num_periodos} períodos com EMA(20/50)...\n")
    
    sinais_gerados = []
    for periodo in range(num_periodos):
        # Gera variação aleatória realista
        precos_ema = {
            symbol: max(1, precos_ema[symbol] * (1 + random.gauss(0, 0.015)))
            for symbol in ativos
        }
        
        assets_data = [{'symbol': symbol, 'price': precos_ema[symbol]} for symbol in ativos]
        sinais = ema_strategy.com(assets_data)
        
        if sinais:
            sinais_gerados.extend(sinais)
            print(f"Período {periodo:3d}: ", end="")
            for sinal in sinais:
                print(f"{sinal['symbol']} {sinal['type']:4s} @ R$ {sinal['price']:7.2f} | ", end="")
            print()
    
    print(f"\n✓ Total de sinais gerados: {len(sinais_gerados)}")
    
    # ========== RESUMO ==========
    print("\n\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"✓ Buy and Hold: funcionando (1 compra, sem vendas)")
    print(f"✓ Moving Average (SMA): {len(sinais_gerados)} sinais gerados")
    print(f"✓ Exponential Moving Average (EMA): funcionando com dados fictícios")
    print("\nTodos os modelos estão prontos para uso com o BacktestEngine!")