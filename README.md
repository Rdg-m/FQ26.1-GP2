# Back-da-dev


## FQ26.1-GP2
**FEA.dev Backtesting Lab** — Protótipos rápidos e backtesting quantitativo para estudantes e investidores curiosos.

## Sumário
- [Sobre o Projeto](#sobre-o-projeto)
- [Construído Com](#constru%C3%ADdo-com)
- [Começando](#come%C3%A7ando)
  - [Pré-requisitos](#pr%C3%A9-requisitos)
  - [Instalação](#instala%C3%A7%C3%A3o)
  - [Configuração](#configura%C3%A7%C3%A3o)
- [Uso](#uso)
  - [API Python](#api-python)
  - [CLI](#cli)
- [Documentação da API](#documenta%C3%A7%C3%A3o-da-api)
- [Testes](#testes)
- [Contribuindo](#contribuindo)
- [Licença](#licen%C3%A7a)

## Sobre o Projeto
Este repositório é um projeto de estudante da FEA.dev para backtesting rápido e prototipagem de estratégias quantitativas. O código auxilia membros da liga a explorar ideias de trading, validar sinais e gerar resumos de desempenho a partir de dados históricos.

Ele combina ingestão de dados, limpeza, execução de estratégia e visualização de resultados em um fluxo simples. O objetivo é tornar a pesquisa quant inicial rápida de iterar, mantendo conexão com conceitos reais de mercado como comissão, drawdown e resultados de trades.

## Construído Com
- Python `>=3.11`
- `pandas` para manipulação de séries temporais e pipeline de dados
- `numpy` para operações numéricas
- `matplotlib` para visualização de resultados
- `requests` para acesso a APIs
- `yfinance` para download de histórico de mercado
- `pytest` para cobertura de testes

## Começando

### Pré-requisitos
- Python `3.11` ou superior
- gerenciador de pacotes `pip`
- Opcionalmente, uma ferramenta de ambiente virtual: `venv`, `virtualenv` ou `pipenv`

### Instalação
A partir da raiz do repositório:

```bash
python -m pip install -e .
```

Se preferir um ambiente dedicado:

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.\.venv\Scripts\activate  # Windows
python -m pip install -e .
```

### Configuração
Este projeto não requer variáveis de ambiente especiais por padrão.

- Use `yfinance` como fonte padrão de dados
- Coloque arquivos locais em `./data/` ao carregar do disco
- Se precisar de outras fontes de dados, instale dependências opcionais manualmente

> Se seu fluxo de trabalho usar API externa ou credenciais privadas, adicione esses detalhes aqui mais tarde.

## Uso

### API Python
Importe o ponto de entrada público do pacote:

```python
from back_da_dev import run_standard_backtest, load_and_clean, list_strategies

raw_df = load_and_clean(indice="PETR4.SA", fonte="yfinance", tempo="5y")

result = run_standard_backtest(
    data=raw_df,
    strategy="buy_and_hold",
    initial_capital=10000.0,
    commission=0.001,
    save_graphs=False,
    save_log=False,
)

print(result.metrics)
```

Gere um relatório após um backtest:

```python
from back_da_dev import generate_backtest_report

report = generate_backtest_report(
    engine=result.engine,
    output_dir="./results",
    prefix="feadev_backtest",
)
print(report.graph_paths)
print(report.log_path)
```

Graphing and report options
---------------------------

The interface supports selecting which charts to export and which output formats to save. Supported chart names include: `equity_curve`, `drawdown`, `cumulative_returns`, `volatility`, `bollinger`, `rsi`, `time_series`.

Example (API):

```python
from back_da_dev import generate_backtest_report

report = generate_backtest_report(
  engine=result.engine,
  output_dir='./results',
  charts=['equity_curve','rsi','bollinger'],
  formats=('png','svg'),
)
```

Example (CLI):

```bash
python -m back_da_dev --indice PETR4.SA --strategy ma --output-dir ./results --charts equity_curve rsi bollinger --chart-formats png svg
```

### CLI
Execute o pacote como módulo:

```bash
python -m back_da_dev --indice PETR4.SA --strategy ma --initial-capital 10000 --output-dir ./results
```

Opções de exemplo:
- `--indice`: símbolo do ticker para carregar via yfinance
- `--strategy`: `buy_and_hold`, `ma` ou `ema`
- `--initial-capital`: capital inicial
- `--commission`: taxa de corretagem por operação
- `--output-dir`: onde gráficos e logs serão salvos
- `--no-graphs`: desativa geração de gráficos
- `--no-log`: desativa geração de arquivo de log

## Documentação da API
O pacote público expõe o fluxo principal de backtesting:

- `BacktestEngine` — motor principal para executar simulações de estratégia
- `load_data(...)` — carrega dados históricos de arquivos locais ou `yfinance`
- `clean_data(...)` — limpa, normaliza e valida dados carregados
- `load_and_clean(...)` — fluxo combinado de carregamento e limpeza
- `resolve_strategy(...)` — instancia uma estratégia embutida pelo nome
- `run_standard_backtest(...)` — executa um backtest e retorna métricas
- `generate_backtest_report(...)` — salva gráficos e logs para uma execução concluída
- `save_backtest_log(...)` — serializa métricas e histórico de trade em `.log`
- `list_strategies()` — lista nomes de estratégias disponíveis

## Testes
Execute a suíte de testes do repositório com:

```bash
pytest -q
```

Este projeto inclui testes para:
- comportamento do motor de backtest
- geração de sinais das estratégias
- imports do pacote
- fluxos da interface
- sanidade de empacotamento

## Contribuindo
Membros da FEA.dev e contribuidores externos são bem-vindos.

- Faça um fork do repositório
- Crie uma branch descritiva
- Abra um pull request com sua feature ou correção
- Inclua testes e atualize a documentação quando necessário
- Reporte bugs via issues se o comportamento diferir do esperado

## Licença
Este projeto é licenciado sob a Licença MIT.

Veja [LICENSE](./LICENSE) para detalhes.

