# Fluxograma de Estratégia - Sistema de Backtesting

## 1. Visão Geral do Fluxo em Cascata

A interação entre arquivos funcionará com o seguinte modelo de cascata:

```
┌─────────────────────────────────────────────────────────────────┐
│                      PONTO DE ENTRADA                           │
│                      (main.py)                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTERFACE DO USUÁRIO                         │
│              (code/interface/interface.py)                      │
│  - Exibe opções de operações disponíveis                       │
│  - Captura escolhas do usuário                                 │
│  - Roteia para módulo apropriado                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              ORQUESTRAÇÃO DO BACKTEST PRINCIPAL                 │
│          (code/backtesting/backtesting_main.py)                │
│  - Coordena todo o processo de backtesting                     │
│  - Gerencia capital e portfolio                                │
│  - Executa ordens de compra/venda                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│  CARREGAMENTO DE DADOS   │   │  IMPLEMENTAÇÃO DA        │
│  (load.py)               │   │  ESTRATÉGIA DE NEGÓCIOS  │
│                          │   │  (estrategy.py)          │
│ - Lê múltiplos formatos  │   │                          │
│   (CSV, XLSX, JSON, TXT) │   │ - Define regras de entrada│
│ - Acessa APIs financeiras│   │ - Define regras de saída │
│ - Retorna dataframes     │   │ - Calcula indicadores    │
└──────────┬───────────────┘   │ - Gera sinais de negócio │
           │                   └──────────────────────────┘
           ▼
┌──────────────────────────┐
│  LIMPEZA DE DADOS        │
│  (clean.py)              │
│                          │
│ - Trata valores ausentes │
│ - Converte tipos de dados│
│ - Normaliza dados        │
│ - Valida consistência    │
└──────────┬───────────────┘
           │
           └──────────────────────┬─────────────────────┐
                                  │                     │
                                  ▼                     ▼
                        ┌──────────────────────┐ ┌─────────────────┐
                        │  PROCESSAMENTO DO    │ │  CÁLCULO DE     │
                        │  BACKTEST            │ │  INDICADORES    │
                        │                      │ │                 │
                        │ - Itera períodos     │ │ - Médias móveis │
                        │ - Aplica estratégia  │ │ - RSI           │
                        │ - Atualiza portfolio │ │ - MACD          │
                        └──────────┬───────────┘ │ - Outros        │
                                   │             └─────────────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ CÁLCULO DE RESULTADOS│
                        │                      │
                        │ - Lucro/Prejuízo     │
                        │ - Retorno %          │
                        │ - Drawdown           │
                        │ - Métricas de risco  │
                        └──────────┬───────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                GERAÇÃO DE GRÁFICOS E LOGS                       │
│              (code/graphing/graphing.py)                        │
│  - Gráficos de desempenho                                       │
│  - Tabelas de resultados                                        │
│  - Gráficos de barras, linhas, pizza                            │
│  - Exportação em múltiplos formatos                             │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Fluxo de Dados Detalhado

### 2.1 Entrada de Dados
- **Localização**: Dados depositados em `./data/`
- **Formatos Suportados**: CSV, XLSX, JSON, TXT
- **APIs**: Integrações com provedores de dados financeiros
- **Saída**: Dataframes pandas com dados históricos

### 2.2 Processamento de Dados
1. **Carregamento** (load.py):
   - Importar bibliotecas (pandas, numpy, etc.)
   - Definir caminhos de arquivo e credenciais de API
   - Ler dados e armazená-los em dataframes

2. **Limpeza** (clean.py):
   - Tratar valores ausentes (NaN, None)
   - Converter tipos de dados (string → float, int, datetime)
   - Normalizar dados (escala, formatação)
   - Validar integridade dos dados

### 2.3 Processamento do Backtest
1. **Estratégia** (estrategy.py):
   - Calcular indicadores técnicos
   - Aplicar regras de entrada (condições de compra)
   - Aplicar regras de saída (condições de venda)
   - Gerar sinais de negócio

2. **Execução** (backtesting_main.py):
   - Iterar sobre períodos de tempo
   - Executar sinais de compra/venda
   - Atualizar capital disponível
   - Registrar histórico de posições
   - Calcular métricas de desempenho

### 2.4 Visualização de Resultados
- Criar gráficos de desempenho
- Gerar tabelas de resumo
- Exportar relatórios
- Salvar logs e histórico

## 3. Pontos de Decisão e Branches

```
┌─────────────────────────────────┐
│   Qual é a ação desejada?       │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┬──────────────┬──────────────┐
      │             │              │              │
      ▼             ▼              ▼              ▼
  Backtest     Carregar     Processar      Visualizar
   (Padrão)   Novos Dados   Dados          Resultados
      │             │              │              │
      └──────────┬──────────────┬──┴──────────┬───┘
                 │              │             │
          [Continuar]     [Continuar]  [Exibir gráficos]
```

## 4. Dependências Entre Módulos

| Módulo | Depende De | Fornece Para |
|--------|-----------|--------------|
| main.py | Nenhum | interface.py |
| interface.py | backtesting_main.py, load.py, graphing.py | Usuário |
| backtesting_main.py | load.py, clean.py, estrategy.py, graphing.py | interface.py |
| load.py | Arquivos de dados externos, APIs | backtesting_main.py, clean.py |
| clean.py | load.py | backtesting_main.py |
| estrategy.py | Nenhum | backtesting_main.py |
| graphing.py | backtesting_main.py (dados de resultado) | interface.py, Arquivos de exportação |

## 5. Fluxo de Execução Passo a Passo

1. **Inicialização**
   - `main.py` é executado
   - Carrega `interface.py`

2. **Seleção de Operação**
   - Usuário escolhe ação padrão (backtest)
   - Interface roteia para `backtesting_main.py`

3. **Carregamento de Dados**
   - `backtesting_main.py` chama `load.py`
   - `load.py` lê dados de `./data/`
   - Retorna dataframes com dados históricos

4. **Limpeza de Dados**
   - `backtesting_main.py` chama `clean.py`
   - `clean.py` processa dataframes
   - Retorna dados limpos e validados

5. **Execução do Backtest**
   - `backtesting_main.py` itera períodos
   - Para cada período, consulta `estrategy.py`
   - `estrategy.py` retorna sinais de compra/venda
   - `backtesting_main.py` executa as ordens
   - Atualiza capital, portfolio e histórico

6. **Cálculo de Resultados**
   - `backtesting_main.py` calcula métricas:
     - Lucro/Prejuízo total
     - Retorno percentual
     - Drawdown máximo
     - Taxa de Sharpe
     - Fator de lucro
     - Outros indicadores de risco

7. **Visualização**
   - `backtesting_main.py` chama `graphing.py`
   - `graphing.py` cria gráficos e tabelas
   - Salva resultados em arquivos
   - Exibe para o usuário via `interface.py`
