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

import os
import pandas as pd
import numpy as np
import requests 
import yfinance as yf
from io import StringIO
from bcb import sgs
from src.dataprocessing.b3 import read_b3

def load_data(caminho=None, formato='csv', indice=None, fonte="yfinance", tempo='10y', comeco=None, fim=None, salvar=False):
      match formato:
        
        case 'csv':
            return pd.read_csv(caminho, index_col=0, parse_dates=True)
        case 'json':
            return pd.read_json(caminho)
        case 'xlsx':
            return pd.read_excel(caminho, index_col=0, engine='openpyxl')
        case 'b3':
              return read_b3(caminho, comeco, tempo, fim)
        case _:
            if formato is not None: 
               raise NotImplementedError("Formato não aceitado!")

    elif indice is not None:
        if fonte == "yfinance":
            if (comeco is not None) and fim is not None:
                df = yf.download(indice, start=comeco, end=fim)
            else:
                df = yf.download(indice, period=tempo)
        
        elif fonte == 'bcb':
            codigo = int(indice)
            df = sgs.get({'Close': codigo}, start=comeco)
            df.index.name = 'Date'
            df['Open'] = df['Close']
            df['High'] = df['Close']
            df['Low'] = df['Close']
            df['Volume'] = 0.0
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        colunas_esperadas = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        for col in colunas_esperadas:
            if col not in df.columns:
                raise KeyError(f"Faltando a coluna '{col}'") 

        df = df[colunas_esperadas]

        if salvar:
            pasta_dados = '../dados'
            if not os.path.exists(pasta_dados):
                os.makedirs(pasta_dados)
                
            arquivo = str(indice)
            caminho_salvar = f"{pasta_dados}/{arquivo}.csv"
            df.to_csv(caminho_salvar)
            
        return df
        
    else:
        raise ValueError("Precisamos de um lugar para busca esse dado")