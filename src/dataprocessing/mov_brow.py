import random as rd
from typing import Callable
import math 

def brow(t):
    return rd.normalvariate(0, t) 

def MBG(m:float | int, o:float | int, seed:int = 42) -> tuple[Callable[..., float], Callable[..., float]]:
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



def solve_type(*a) -> Callable:
    '''
    Descobre o tipo de a e retorna uma função que aplica f sobre o valor/estrutura.
    O objetivo é atualizar preços ou vetores com um step gerado por f.
    '''
    if len(a) == 0:
        raise ValueError('solve_type precisa de pelo menos um argumento')

    value = a[0] if len(a) == 1 else a

    if isinstance(value, (int, float)):
        return lambda f, *args: f() * args[0]

    if isinstance(value, (tuple, list)):
        return lambda f, *args: [f() * item for item in args[0]]

    if isinstance(value, np.ndarray):
        return lambda f, *args: args[0] * f()

    if isinstance(value, pd.DataFrame):
        return lambda f, *args: args[0] * f()

    # Fallback: tente aplicar f a cada elemento se for iterável
    try:
        iter(value)
        return lambda f, *args: [f() * item for item in args[0]]
    except TypeError:
        return lambda f, *args: f() * args[0]

def Atualizar_com_browniano(*a):
    '''ideia geral de como seria a implementação na classe, só jogar pra dentro e trocar as referencias pra self.
    a função recebe um vetor provavelmente de ações onde cada ação tem um vetor com ohlcm
    aplicando o mesmo step do movimento para cada vetor ohlcm e diferente pra cada ação, temos um mercado aleatório    '''
    f = solve_type(a)
    MOV, Step = MBG(_params.get('m', 0), _params.get('o', 1))
    return f(Step, *a)

def set_var_regime(s:str, d:dict=_config['mov_brown_parans'])->dict:
    new_d ={}
    match s:
        case 'Y':
            new_d['o'] = d['o']*((240)**(.5))
        case 'm':
            new_d['o'] = d['o']*((20)**(.5))
        case 'd':
            new_d['o'] = d['o']
        case _:
            raise NotImplemented
    new_d['m'] = d['m']
    return new_d


def set_regime(x:float=0, s:str=None, d:dict=_config['mov_brown_parans'])->dict:
    new_d ={}
    if s is not None:
        match s:
            case 'high':
                new_d['m'] = 1
            case 'low':
                new_d["m"] = -1
            case 'stable':
                new_d['m'] = 0
            case _:
                raise ValueError('valor não corresponde aos usados', s)
    else:
        new_d["m"]=x
    new_d['o'] = d.get('o')
    return new_d     



        