"""
Módulo de Limpeza e Preprocessamento de Dados

RESPONSABILIDADES:
- Limpar dados históricos de ativos financeiros
- Tratar valores ausentes (NaN, None, gaps)
- Converter tipos de dados apropriadamente
- Normalizar e validar estrutura de dados
- Remover outliers e dados inválidos
- Preparar dados para processamento de backtest

QUANDO USAR:
- Após carregar dados em load.py
- Antes de usar dados em backtesting_main.py
- Para validar integridade de dados antes de análise

OPERAÇÕES SUPORTADAS:

1. TRATAMENTO DE VALORES AUSENTES
   Estratégias:
   - Forward Fill (ffill): Usar último valor válido
   - Backward Fill (bfill): Usar próximo valor válido
   - Interpolação Linear: Interpolar entre valores
   - Remoção: Descartar linhas incompletas
   
   Casos de uso:
   - Holidays/fins de semana: Forward fill
   - Pequenos gaps de dados: Interpolação
   - Grandes gaps: Reportar e investigar
   - Primeiras/últimas linhas: Remover

2. CONVERSÃO DE TIPOS DE DADOS
   - Data/Timestamp: string → datetime64
   - Preços (Open, High, Low, Close): string → float64
   - Volume: string → int64
   - Adjusted Close: string → float64
   - Divisores e ajustes: int → float
   
   Validações:
   - Datas em formato válido (YYYY-MM-DD ou equivalente)
   - Preços são números positivos
   - Volume é número inteiro não-negativo
   - Relação lógica: Low ≤ Open, Close, High ≤ High

3. NORMALIZAÇÃO DE DADOS
   - Ordenar por data (crescente)
   - Remover duplicatas
   - Validar continuidade temporal
   - Padronizar nomes de colunas
   - Padronizar unidades (ex: centavos para reais)

4. VALIDAÇÃO E INTEGRIDADE
   Checagens:
   - Valores ausentes restantes > limite?
   - Preços fazem sentido (Low ≤ Close ≤ High)?
   - Volumes são positivos?
   - Datas em ordem crescente?
   - Sem duplicatas?
   - Sem valores extremos inválidos?

5. REMOÇÃO DE OUTLIERS
   Métodos:
   - Z-score: Remover valores > 3σ
   - IQR (Interquartile Range): Remover valores extremos
   - % de mudança: Validar movimentos de preço
   - Volume incomum: Investigar picos de volume

FLUXO DE PROCESSAMENTO:

┌─────────────────────────────────────────┐
│  Dataframe Recebido (potencialmente sujo)│
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Converter Tipos de Dados               │
│ (string → float, int, datetime)        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Tratar Valores Ausentes                │
│ (ffill, bfill, interpolação, remoção)  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Validar Integridade (Low ≤ Close ≤ High)│
│ Remover outliers se necessário         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Normalizar e Ordenar Dados            │
│ (nomes de colunas, ordem temporal)    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Gerar Relatório de Limpeza             │
│ (estatísticas, problemas encontrados)  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Dataframe Limpo e Validado            │
│  (pronto para backtesting)             │
└─────────────────────────────────────────┘

EXEMPLOS DE PROBLEMAS COMUNS:

Problema 1: Valores Ausentes em Feriados
- Detecção: Gap de um dia sem dados
- Solução: Forward fill (copiar último valor válido)
- Risco: Pode introduzir bias se não tratado corretamente

Problema 2: Dados com Tipos Incorretos
- Detecção: Conversão falha ou valores inesperados
- Solução: Converter com pandas.to_numeric(), coerce errors
- Validação: Após conversão, confirmar distribuição faz sentido

Problema 3: Valores Extremos (Outliers)
- Detecção: Picos de preço ou volume incomuns
- Investigação: Verificar se são splits ou erros de dados
- Decisão: Remover, manter ou ajustar conforme necessário

Problema 4: Inconsistências de Preço
- Detecção: Low > High ou Close > High
- Cause: Erros de entrada ou inversão de colunas
- Solução: Investigar fonte de dados, corrigir ou excluir

RELATÓRIO DE LIMPEZA:
O módulo deve gerar relatório com:
- Quantidade de linhas originais
- Quantidade de linhas após limpeza
- Valores ausentes tratados (quantidade, estratégia)
- Outliers removidos (quantidade, critério)
- Conversões de tipo (sucesso/falha)
- Alertas ou problemas encontrados
- Estatísticas do dataframe final

DEPENDÊNCIAS:
- pandas: Operações em dataframes
- numpy: Operações numéricas (z-score, IQR)
- scipy: Estatísticas avançadas (se necessário)

EXEMPLO DE USO:
    from code.dataprocessing.clean import clean_data
    
    # Limpar dataframe sujo
    df_clean = clean_data(
        df=df_raw,
        handle_missing='interpolate',
        remove_outliers=True,
        verbose=True
    )
    
    # Retorna dataframe limpo com relatório de processamento

NOTAS:
- Operação não-destrutiva: mantém cópia dos dados originais
- Configurável para diferentes estratégias de limpeza
- Gera logs detalhados de todas as transformações
- Suporta customização via parâmetros
"""