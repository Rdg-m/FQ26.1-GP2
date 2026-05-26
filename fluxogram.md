# Fluxograma de Implementação Atual — FQ26.1-GP2

## 1. Visão Geral Atual do Projeto

O projeto está construindo uma biblioteca de backtesting financeiro com:
- carregamento de dados históricos
- limpeza e validação de séries temporais
- motor de backtesting de ordens e posições
- estratégias básicas de trading
- utilitários de gráficos e indicadores técnicos

Ele ainda não está completo, mas já tem um núcleo de engine funcional e modos de simulação.

## 2. Arquitetura Atual

```
┌────────────────────────────────────────────┐
│         src/interface/interface.py         │
│  - ponto de entrada de interface (stub)    │
│  - atualmente apenas imprime uma mensagem  │
└────────────────────────────┬───────────────┘
                             │
                             ▼
┌────────────────────────────────────────────┐
│    src/backtesting/backtesting_main.py     │
│  - BacktestEngine                           │
│  - execução de BUY/SELL                     │
│  - stop loss / take profit                  │
│  - histórico diário e valor do portfólio    │
│  - modo normal e modo browniano             │
└────────────────────────────┬───────────────┘
                             │
             ┌───────────────┴──────────────┐
             │                              │
             ▼                              ▼
┌──────────────────────────┐       ┌──────────────────────────────────┐
│ src/dataprocessing/load.py │     │ src/backtesting/modelos_pre_implementados.py │
│ - CSV/JSON/XLSX             │     │ - buy_and_hold                         │
│ - yfinance                  │     │ - MA / EMA                             │
│ - valida colunas OHLCV      │     │ - adaptador de sinais                  │
└───────────────────────────┘       └──────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ src/dataprocessing/clean.py                │
│ - converte tipos                            │
│ - trata NaN                                │
│ - remove inconsistências                    │
│ - ordena índice                             │
└────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ src/graphing/graphing.py                    │
│ - plotagem matplolib com temas              │
│ - gráficos de equity e drawdown             │
│ - cálculo de RSI/MACD/Bollinger             │
└────────────────────────────────────────────┘
```

## 3. O que já foi feito

### Módulos implementados

- `BacktestEngine` em `src/backtesting/backtesting_main.py`
  - compra e venda de ordens
  - posições abertas e fechadas
  - atualização de capital
  - histórico diário de portfólio
  - stop loss / take profit
  - simulação browniana e execução normal
- Estratégias em `src/backtesting/modelos_pre_implementados.py`
  - base `estrat`
  - `buy_and_hold`
  - `MA` com SMA
  - `EMA` com EMA
- Carregamento de dados em `src/dataprocessing/load.py`
  - suporte a arquivo local e yfinance
  - validação de colunas mínimas
- Limpeza em `src/dataprocessing/clean.py`
  - conversão de tipos
  - tratamento de NaN
  - remoção de linhas inconsistentes
  - ordenação por índice temporal
- Visualização em `src/graphing/graphing.py`
  - tema de plotagem
  - funções de indicadores técnicos
  - plots de série temporal, equity curve e drawdown
- Testes em `tests/`
  - cobertura do motor de backtest
  - cobertura das estratégias

### Resultados reais existentes

- o backtest funciona em modo browniano
- o engine registra fluxo de posições e cash
- existe suporte básico para estratégia plugável
- o projeto já possui `pyproject.toml` para empacotamento

## 4. O que ainda falta implementar

### Prioridades

1. **Completar integração do fluxo**
   - `load_data` → `clean_data` → `BacktestEngine.run()` → `graphing`
   - fazer `src/interface/interface.py` acessar e dar inicio a pipeline real. 
   - `src/interface/interface.py` deve ser capaz de alterar as _config do backtest
2. **Corrigir empacotamento e imports**
   - imports atualizados para caminhos de pacote instaláveis
   - revisar `src/back_da_dev/__main__.py` e o nome do pacote
3. **Adicionar métricas de desempenho**
   - retorno total e anualizado
   - drawdown máximo
   - Sharpe, Sortino, win rate, profit factor
   - métricas de trades fechados
4. **Melhorar saídas de resultados**
   - exportar gráficos e relatórios
   - salvar CSV / JSON de resultados
   - adicionar logs de execução
5. **Ampliar testes**
   - `load.py` e `clean.py`
   - `graphing.py`
   - empacotamento/pip install
   - fluxo de backtest completo


### Problemas conhecidos

- métricas de backtest permanecem teóricas, sem implementação completa no engine

## 5. Projeto e como usá-lo como biblioteca pip

### O que é o projeto

FQ26.1-GP2 é uma biblioteca Python para backtesting e análise de estratégias financeiras.
Ele reúne:
- processamento de dados históricos
- estratégias de trading protótipo
- motor de execução e simulação
- visualização de resultados

O foco atual é construir uma base reutilizável para desenvolvedores e pesquisadores.

### Pacote pip

O `pyproject.toml` está configurado com:
- `name = "Back_da_dev"`
- `version = "0.0.1"`
- `requires-python = ">=3.11"`
- dependências: `matplotlib`, `numpy`, `pandas`, `requests`, `yfinance`

### Instalação local

No diretório do projeto:

```bash
python -m pip install -e .
```

ou

```bash
python -m pip install .
```

### Importação após instalação

Após instalar, o ideal é importar pelo nome do pacote:

```python
from backtesting.backtesting_main import BacktestEngine
from dataprocessing.load import load_data
from dataprocessing.clean import clean_data
from graphing.graphing import plot_equity_curve
```

> Atenção: antes de publicar, verifique que os imports usem caminhos de pacote instaláveis.

### Exemplo rápido

```python
from dataprocessing.load import load_data
from dataprocessing.clean import clean_data
from backtesting.backtesting_main import BacktestEngine
from backtesting.modelos_pre_implementados import buy_and_hold

raw = load_data(indice='PETR4.SA', fonte='yfinance', tempo='1mo')
clean = clean_data(raw, handle_missing='ffill')
engine = BacktestEngine(clean, ['PETR4.SA'], initial_capital=10000.0, commission=0.001)
strategy = buy_and_hold(10000.0)
engine._configs['dado_real'] = True
engine.run(strategy)
print(engine.cash, engine.portfolio_value)
```

### O que precisa antes de publicar no PyPI

- remoção de imports `src.*` do código ativo
- interface CLI funcional
- documentação no README
- testes de empacotamento
- métricas e relatórios completos
- validação dos módulos importáveis
