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
    from src.dataprocessing.clean import clean_data
    
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
import pandas as pd
import numpy as np
def clean_data(df,handle_missing='ffill',remove_outliers=False,verbose=True):
   df_limpo=df.copy()
   linhas_original=len(df_limpo)
   dados_faltando=0
   outliers=0
   alertas=[]
   try:
      df_limpo.index=pd.to_datetime(df_limpo.index)
   except Exception as e:
      alertas.append(f"Erro Datetime:{e}")
   colunas=['Open','High','Low','Close','Volume']
   for col in colunas:
      if col not in df_limpo.columns:
         continue

      df_limpo[col]=pd.to_numeric(df_limpo[col],errors='coerce')
   df_limpo["Volume"]=df_limpo["Volume"].fillna(0).astype('int64')
   df_limpo=df_limpo[~df_limpo.index.duplicated()]
   df_limpo=df_limpo.sort_index()
   nas_original=df_limpo.isna().sum().sum()
   if(nas_original>0):
      if(handle_missing=='ffill'):
         df_limpo=df_limpo.ffill()
      elif(handle_missing=='bfill'):
         df_limpo=df_limpo.bfill()
      elif(handle_missing=='interpolate'):
         df_limpo=df_limpo.interpolate(method='time')
      elif(handle_missing=="drop"):
         df_limpo=df_limpo.dropna()
      else:
         alertas.append(f"Nao foi possivel usar {handle_missing}, retirou-se os NaN")
         df_limpo=df_limpo.dropna()
      dados_faltando=nas_original-df_limpo.isna().sum().sum()
   inconsistentes=df_limpo[(df_limpo["High"]<df_limpo["Low"])|(df_limpo['Close']<0)|(df_limpo["High"]<0)|(df_limpo["Low"]<0)]
   if not (inconsistentes.empty):
      alertas.append(f"Inconsistencias em: {len(inconsistentes)} linhas")
      df_limpo=df_limpo.drop(inconsistentes.index)

   if remove_outliers:
      retornos=df_limpo["Close"].pct_change().dropna()
      z_scores=np.abs((retornos-retornos.mean())/retornos.std())
      outliers_encontrados=z_scores[z_scores>3] 
      if not outliers_encontrados.empty:
         outliers=len(outliers_encontrados) 
         alertas.append(f"Retiramos {outliers} outliers, cheque para ver se não estamos retirando dados demais.")
         df_limpo = df_limpo.drop(outliers_encontrados.index) 

   linhas_finais=len(df_limpo)
   
   report_data = {
      "Linhas_Originais": [linhas_original],
      "Linhas_Finais": [linhas_finais],
      "NaN_Tratados": [dados_faltando],
      "Outliers_Removidos": [outliers],
      "Alertas": ["; ".join(alertas) if alertas else "Sem alertas"]
   }
   df_report = pd.DataFrame(report_data)
   if verbose:
      print(f"Linhas Originais: {linhas_original} | Finais: {linhas_finais}")
      print(f"NaNs tratados: {dados_faltando} | Outliers removidos: {outliers}")
      print(f"Alertas: {'; '.join(alertas) if alertas else 'Nenhum'}")

   return df_limpo, df_report