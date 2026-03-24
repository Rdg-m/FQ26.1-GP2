#funções para carregar os dados históricos dos ativos a serem negociados, como por exemplo, ler arquivos CSV, acessar APIs de dados financeiros, etc. Essas funções devem ser flexíveis o suficiente para permitir a leitura de diferentes formatos de dados e devem ser fáceis de usar para o usuário final. Elas devem conter as seguintes etapas:
#Muito importante load conseguir ler facilmente xlsx, csv, txt, json.
#1. Importar as bibliotecas necessárias para a leitura dos dados, como por exemplo,pandas, numpy, etc.
#2. Definir as variáveis necessárias para a leitura dos dados, como por exemplo, o caminho do arquivo CSV, a URL da API, as credenciais de acesso, etc.
#3. Ler os dados históricos dos ativos a serem negociados e armazená-los em dataframes.
#4. Tratar os dados usando as funções de limpeza e preprocessamento do arquivo clean.py, como por exemplo, lidar com valores ausentes, converter os tipos de dados, etc.
#5. Retornar os dataframes com os dados históricos dos ativos a serem negociados para serem usados nas etapas seguintes do backtest.