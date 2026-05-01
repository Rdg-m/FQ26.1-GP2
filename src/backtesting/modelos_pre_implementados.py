"""
esse arquivo será usado para guardar o código de modelos financeiros básicos para uso de teste das funções do projeto e benchmark
ele será chamado por backtest_main
reponderá a backtest_main tambem com sinais de compra e venda de ativos conforme documentado na documentação do backtest
"""

from typing import Any


class estrat:
    def __init__(self, saldo) -> None:
        self.saldo = saldo
        self. memoria = {}


class buy_and_hold(estrat):
    '''
    pegar todas as ações do dia e gerar buy-orders a fim de gastar a mesma quantia em cada ação disponivel
    não fazer mais nada
    '''

    def __init__(self, saldo) -> None:
        super().__init__(saldo)
        self.compradas = False

    def com(self, *a):
        if self.compradas:
            return None
        else:
            self.compradas = True
            # retornar buy orders das ações usando 1/k do saldo
            pass


class MA(estrat):
    ''' comprar e vender a depender da moving AVG de cada asset'''
    def __init__(self, saldo) -> None:
        super().__init__(saldo)
    
    def com(*a):
        self.add_mem(*a) #coloca preço na memória para calc MA
        pass





