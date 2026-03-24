A interação entre arquivos funcionará com o seguinte modelo de cascata:
1. Os dados necessários devem ser depositados na pasta ./data no repo.
1. main.py será chamada
1. Ao se escolher a ação padrão do programa na interface o controle será passado para o ./code/backtesting/backtesting_main.py
1. Os dados necessários serão carregados pelo ./code/dataprocessing/load.py e processados pelo ./code/dataprocessing/clean.py e repassados para o ./code/backtesting/backtesting_main.py
1. Após o setup inicial o backtest será processado usando as regras/sinais de compra e venda estabelecidas em ./code/estrategy.py
1. Ao final do processo as métricas e o histórico serão  resumidos em uma bateria de gráficos e logs criados pelo arquivo ./code/graphing/graphing.py usando os dados resultandes de backtesting_main.py