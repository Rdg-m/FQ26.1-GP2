import os
import pandas as pd
import numpy as np
import requests 
import yfinance as yf
from io import StringIO
from bcb import sgs

def load_data(caminho=None, formato='csv', indice=None, fonte="yfinance", tempo='10y', comeco=None, fim=None, salvar=False):
    if caminho is not None:
        if formato == 'csv':
            return pd.read_csv(caminho, index_col=0, parse_dates=True)
        elif formato == 'json':
            return pd.read_json(caminho)
        elif formato == 'xlsx':
            return pd.read_excel(caminho, index_col=0, engine='openpyxl')
        else:
            raise TypeError("Formato não aceitado!")

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