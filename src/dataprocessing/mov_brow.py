import random as rd
from typing import Callable
import math 

def brow(t):
    return rd.normalvariate(0, t) 


def MBG(m:float | int, o:float | int, seed:int = 40) -> tuple[Callable[..., float], Callable[..., float]]:
    rd.seed(seed)
    # seta params da série
    def M(t:float | int)-> float:
        # modela um andar dessa série
        #lembrar de sempre multiplicar o retorno ao preço em t_0
        return math.exp((m-(o**2)/2)*t + o*brow(t))
    
    def step()-> float:
        #retorna o fator de atualização num tempo discreto 1
        return math.exp((m-(o**2)/2) + o*brow(1))

    
    return M, step


