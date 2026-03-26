"""
Módulo de Carregamento de Dados - Importação de Dados Históricos

RESPONSABILIDADES:
- Ler dados históricos de múltiplos formatos de arquivo
- Acessar APIs de dados financeiros
- Validar integridade de dados carregados
- Chamar funções de limpeza do módulo clean.py
- Retornar dataframes pandas com dados históricos prontos para uso

FORMATOS SUPORTADOS:
- CSV (Comma-Separated Values)
- XLSX (Excel spreadsheet)
- JSON (JavaScript Object Notation)
- TXT (Texto com delimitadores variáveis)

CARACTERÍSTICAS:
- Suporte a múltiplas fontes de dados (arquivos locais e APIs)
- Flexível para diferentes estruturas de dados
- Fácil de usar para usuários finais
- Integração com APIs financeiras (yahoofinance, alpha_vantage, etc.)

ETAPAS DE EXECUÇÃO:

1. IMPORTAÇÃO DE BIBLIOTECAS
   - pandas: Manipulação de dados em dataframes
   - numpy: Operações numéricas
   - json: Leitura de arquivos JSON
   - openpyxl/xlrd: Leitura de arquivos Excel
   - requests: Acesso a APIs web
   - datetime: Manipulação de datas

2. DEFINIÇÃO DE VARIÁVEIS
   - Caminho do arquivo CSV/XLSX/JSON/TXT
   - URLs e credenciais de APIs
   - Tokens de autenticação
   - Parâmetros de período de dados
   - Símbolos de ativos financeiros

3. LEITURA DE DADOS
   - Detectar formato automaticamente ou usar parâmetro explícito
   - CSV: pandas.read_csv()
   - XLSX: pandas.read_excel()
   - JSON: pandas.read_json() ou json.load()
   - TXT: pandas.read_csv() com delimitadores customizados
   - API: requests.get() + processamento de resposta

4. VALIDAÇÃO INICIAL
   - Verificar se dados foram carregados corretamente
   - Confirmar colunas esperadas existem
   - Validar tipos de dados básicos

5. PROCESSAMENTO COM clean.py
   - Chamar funções de clean.py para tratar dados
   - Lidar com valores ausentes
   - Converter tipos de dados
   - Normalizar valores

6. RETORNO DE DADOS
   - Retornar dataframe com dados históricos limpos
   - Incluir metadados (período, ativo, fonte)
   - Garantir que dados estão prontos para backtest

ESTRUTURA ESPERADA DOS DADOS:
- Índice: Data/Timestamp (YYYY-MM-DD HH:MM:SS)
- Colunas mínimas:
  - Open (Abertura): Preço de abertura
  - High (Alta): Preço máximo do período
  - Low (Baixa): Preço mínimo do período
  - Close (Fechamento): Preço de fechamento
  - Volume: Quantidade transacionada

OPÇÕES DE COLUNA ADICIONAIS:
- Adjusted Close (Fechamento ajustado para splits)
- Dividends (Dividendos distribuídos)
- Stock Splits (Desdobramentos de ações)

TRATAMENTO DE ERROS:
- Arquivo não encontrado: Lançar exceção com mensagem clara
- Formato inválido: Detectar e relatar
- Dados ausentes: Registrar e relatar ao usuário
- APIs indisponíveis: Tentar nova conexão ou usar cache local

DEPENDÊNCIAS:
- pandas, numpy: Processamento de dados
- API clients: Acesso a dados externos
- clean.py: Processamento de dados

EXEMPLO DE USO:
    from src.dataprocessing.load import load_data
    
    # Carregar de arquivo CSV
    df = load_data(filepath='./data/PETR4.csv', format='csv')
    
    # Carregar de API
    df = load_data(symbol='PETR4', source='yfinance', period='5y')
    
    # Retorna dataframe com dados históricos limpos e validados

NOTAS:
- Dados são retornados como dataframes pandas para uso em backtesting
- Todas as operações devem ser reversíveis (não modificam dados originais)
- Manter log de dados carregados para auditoria
- Suportar carregamento de múltiplos ativos simultaneamente
"""


import pandas as pd
from pathlib import Path


def _to_float_b3(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    if s == '' or s == '0':
        return 0.0
    only_digits = ''.join(ch for ch in s if ch.isdigit())
    if only_digits == '':
        return 0.0
    return int(only_digits) / 100.0


def _to_int(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    only_digits = ''.join(ch for ch in s if ch.isdigit())
    if only_digits == '':
        return 0
    return int(only_digits)

def _load_B3_bib(path = None) -> dict:
    from json import load
    path = r'src/dataprocessing/tabela_de_leitura_b3.json' if path == None else path
    with open(path, 'r') as file:
        return load(file)

def load_cot_hist_b3(filepath: str) -> pd.DataFrame:
    """
    Carrega arquivo COTAHIST B3 em layout fixed-width.
    Retorna DataFrame com coluna `data` (não índice).
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    # Base no layout B3 COTAHIST (campos relevantes)
    colspecs = [
        (0, 2),    # TP_REGISTRO
        (2, 10),   # DATA
        (10, 12),  # COD_BDI
        (12, 24),  # COD_NEG
        (24, 27),  # TP_MERC
        (27, 39),  # NOME
        (39, 49),  # ESPECI
        (49, 52),  # PRAZOT
        (52, 56),  # MODREF
        (56, 69),  # PREABE
        (69, 82),  # PREMAX
        (82, 95),  # PREMIN
        (95, 108), # PREMED
        (108, 121),# PREULT
        (121, 134),# PREOFC
        (134, 147),# PREOFV
        (147, 152),# TOTPAP
        (152, 170),# QUATOT
        (170, 188),# VOLTOT
        (188, 201),# PREEXE
        (201, 202),# INDOPC
        (202, 210),# DATVEN
        (210, 217),# FATCOT
        (217, 230),# PTOEXE
        (230, 242),# CODISI
        (242, 245),# DISMES
    ]

    names = [
        "TP_REGISTRO",
        "DATA",
        "COD_BDI",
        "COD_NEG",
        "TP_MERC",
        "NOME",
        "ESPECI",
        "PRAZOT",
        "MODREF",
        "PREABE",
        "PREMAX",
        "PREMIN",
        "PREMED",
        "PREULT",
        "PREOFC",
        "PREOFV",
        "TOTPAP",
        "QUATOT",
        "VOLTOT",
        "PREEXE",
        "INDOPC",
        "DATVEN",
        "FATCOT",
        "PTOEXE",
        "CODISI",
        "DISMES",
    ]

    df = pd.read_fwf(filepath, colspecs=colspecs, names=names, dtype=str, header=None)

    # Filtrar somente registros de negociação usual (tp registro = 01)
    df = df[df["TP_REGISTRO"].str.strip() == "01"].copy()

    # Data e símbolos
    df["data"] = pd.to_datetime(df["DATA"].str.strip(), format="%Y%m%d", errors="coerce")
    df["ticker"] = df["COD_NEG"].str.strip()
    df["isin"] = df["CODISI"].str.strip()

    # Preços e volume
    df["open"] = df["PREABE"].apply(_to_float_b3)
    df["high"] = df["PREMAX"].apply(_to_float_b3)
    df["low"] = df["PREMIN"].apply(_to_float_b3)
    df["close"] = df["PREULT"].apply(_to_float_b3)
    df["volume"] = df["VOLTOT"].apply(_to_int)
    df["value"] = df["QUATOT"].apply(_to_float_b3)

    # Validações básicas
    if df["data"].isna().any():
        raise ValueError("Linha(s) com DATA inválida encontradas no arquivo COTAHIST.")

    # Retorno com data como coluna (solicitado)
    df_out = df[
        ["data", "ticker", "isin", "TP_MERC", "NOME", "ESPECI", "open", "high", "low", "close", "volume", "value"]
    ].copy()

    df_out = df_out.sort_values("data").reset_index(drop=True)

    # Checagem de integridade de preços
    invalid_price = (df_out["low"] > df_out["high"]) | (df_out["low"] > df_out["close"]) | (df_out["high"] < df_out["close"])
    if invalid_price.any():
        raise ValueError("Inconsistência de valores de preço detectada (low/high/close).")

    return df_out



