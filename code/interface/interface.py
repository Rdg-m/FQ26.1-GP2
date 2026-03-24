"""
Interface do Usuário - Menu e Interação com o Programa

RESPONSABILIDADES:
- Exibir menu principal com opções de operações disponíveis
- Capturar escolhas do usuário via terminal
- Rotear requisições para os módulos apropriados
- Fornecer feedback visual ao usuário
- Permitir fácil adição de novas operações no futuro

OPERAÇÕES SUPORTADAS:
1. Backtest (Operação Padrão)
   - Carrega dados via load.py
   - Processa dados via clean.py
   - Executa backtest via backtesting_main.py
   - Exibe resultados via graphing.py

2. Carregar Novos Dados
   - Chama load.py para ler dados de múltiplos formatos
   - Chama clean.py para validar dados

3. Processar e Analisar
   - Aplica estratégia via estrategy.py
   - Calcula indicadores técnicos
   - Exibe análise prévia

4. Visualizar Resultados Anteriores
   - Chama graphing.py para renderizar gráficos
   - Exibe tabelas de resumo

FLUXO DE INTERFACE:
1. Inicializa e exibe menu principal
2. Aguarda entrada do usuário
3. Valida entrada
4. Roteia para módulo apropriado
5. Recebe resultados
6. Exibe resultados formatados
7. Retorna ao menu (ou sai se solicitado)

DEPENDÊNCIAS EXTERNAS:
- code.backtesting.backtesting_main (orquestração principal)
- code.dataprocessing.load (carregamento de dados)
- code.dataprocessing.clean (limpeza de dados)
- code.graphing.graphing (visualização de resultados)

CARACTERÍSTICAS:
- Flexível e extensível para novos tipos de operações
- Fácil de usar para usuários finais
- Valida todas as entradas antes de processar
- Fornece mensagens de erro claras

NOTAS:
- Mantém o programa no escopo de responsabilidade de interface
- Toda lógica complexa fica em módulos especializados
- Permite experimentação interativa do usuário
"""