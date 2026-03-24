#Será o principal arquivo do programa sendo responsável por fazer o backtest da estratégia implementada no arquivo estratégia.py e por chamar as funções da interface para mostrar os resultados para o usuário. Ele deve ser flexível o suficiente para permitir a adição de novas estratégias no futuro e deve ser fácil de usar para o usuário final. Ele deve conter as seguintes etapas:
#1. Importar as bibliotecas necessárias para o backtest, como por exemplo, pandas, numpy, matplotlib, etc.
#2. Importar as funções criadas em outros arquivos, como por exemplo, as funções de leitura de dados, as funções de cálculo de indicadores, as funções de execução de ordens, etc.
#3. Definir as variáveis necessárias para o backtest, como por exemplo, o capital inicial, o período de tempo, os ativos a serem negociados, etc.
#4. Ler os dados históricos dos ativos a serem negociados e armazená-los em dataframes.
#5. Calcular os indicadores necessários para a estratégia, como por exemplo, médias móveis, RSI, MACD, etc.
#6. Executar as ordens de compra e venda de acordo com a estratégia implementada, atualizando o capital disponível e o portfólio de ativos.
#7. Calcular os resultados do backtest, como por exemplo, o lucro ou prejuízo total, o retorno percentual, o drawdown, etc.
#8. Chamar as funções do arquivo de graphing para mostrar os resultados do backtest para o usuário, como por exemplo, gráficos de desempenho, tabelas de resultados, etc.