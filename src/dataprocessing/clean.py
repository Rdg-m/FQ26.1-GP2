import pandas as pd
import numpy as np
def clean_data(df,handle_missing='ffill',remove_outliers=False,verbose=True) -> tuple[pd.DataFrame, pd.DataFrame]:
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
      if col in df.columns:
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
   df_limpo.columns = df_limpo.columns.str.lower()
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