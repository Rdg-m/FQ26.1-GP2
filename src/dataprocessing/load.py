import os
import pandas as pd
import yfinance as yf


def _flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex) and df.columns.nlevels == 2:
        tickers = df.columns.get_level_values(1)
        if tickers.nunique() == 1:
            return df.copy().set_axis(df.columns.get_level_values(0), axis=1)
        raise ValueError(
            "Os dados do yfinance contêm múltiplos tickers. "
            "O sistema atualmente suporta apenas um ticker por vez."
        )
    return df


def load_data(caminho=None, formato='csv', indice=None, fonte="yfinance", tempo='10y', comeco=None, fim=None, salvar=False, de_yfinance=False):
    if caminho is not None:
        if formato == 'csv':
            df = pd.read_csv(caminho, index_col=0, parse_dates=True)
        elif formato == 'json':
            df = pd.read_json(caminho)
        elif formato == 'xlsx':
            df = pd.read_excel(caminho, index_col=0, engine='openpyxl')
        else:
            raise TypeError("Formato não aceito!")

        if salvar:
            pasta_dados = os.path.join(os.getcwd(), 'dados')
            if not os.path.exists(pasta_dados):
                os.makedirs(pasta_dados)
            arquivo = os.path.splitext(os.path.basename(caminho))[0]
            caminho_salvar = f"{pasta_dados}/{arquivo}.csv"
            df.to_csv(caminho_salvar)

        return df

    elif indice is not None:
        if fonte == "yfinance":
            if (comeco is not None) and fim is not None:
                df = yf.download(indice, start=comeco, end=fim)
            else:
                df = yf.download(indice, period=tempo)
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
        
        elif fonte == 'bcb':
            try:
                from bcb import sgs
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "The 'bcb' dependency is required for fonte='bcb'. Install it manualmente se precisar dessa fonte."
                ) from exc
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
            pasta_dados = os.path.join(os.getcwd(), 'dados')
            if not os.path.exists(pasta_dados):
                os.makedirs(pasta_dados)
                
            arquivo = str(indice)
            caminho_salvar = f"{pasta_dados}/{arquivo}.csv"
            df.to_csv(caminho_salvar)
            
        return df
        
    else:
        raise ValueError("Precisamos de um lugar para busca esse dado")