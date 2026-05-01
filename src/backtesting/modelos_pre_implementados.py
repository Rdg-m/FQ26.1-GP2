"""
esse arquivo será usado para guardar o código de modelos financeiros básicos para uso de teste das funções do projeto e benchmark

Vamos tratar os modelos aqui como modelos que seriam implementados para uso do código que estamos escrevendo, então faz sentido que eles chamem os métodos que desenvolveremos
Ou eles sejam usados pelo backtest, depende da lógica de OOP.
"""

from typing import Any


class estrat:
    def __init__(self, saldo) -> None:
        self.saldo = saldo
        self. memoria = None


    def com(*a):
        pass


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
    def __init__(self, saldo, MA_compra, MA_venda) -> None:
        super().__init__(saldo)
        self.politica = (MA_compra, MA_venda)
    
    def com(self, *a):
        self.add_mem(*a) #coloca preço na memória para calc MA
        
        if (p:= self.decisao()) is True:
            # retornar buy orders
            pass
        elif p is False:
            # retornar sell orders
            pass
        else:
            #fazer nada
            return None

    def calc_MA(self):
        #testar se já está calculado
        pass

    def add_mem(self, *a):
        #lembrar de reforçar invariantes
        pass

    def decisao(self):
        '''retorna comprar ou vender ou esperar'''
        MA = self.calc_MA()
        compra, venda = self.politica

        if MA>compra:
            return True
        
        if MA<venda:
            return False
        
        return None


class EMA(MA):
    '''mesma estrat de MA, mas com moving AVG exponencial'''
    def calc_MA(self):
        #calc moving AVG exp
        pass
         