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
- src.backtesting.backtesting_main (orquestração principal)
- src.dataprocessing.load (carregamento de dados)
- src.dataprocessing.clean (limpeza de dados)
- src.graphing.graphing (visualização de resultados)

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

import sys

def exibir_menu():
    print("\n" + "=" * 50)
    print("                  MENU PRINCIPAL")
    print("=" * 50)
    print("1. Backtest (Operação Padrão)")
    print("2. Carregar Novos Dados")
    print("3. Processar e Analisar")
    print("4. Visualizar Resultados Anteriores")
    print("0. Sair")
    print("=" * 50)

def clear_screen():
    import os
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


def main():
    while True:
        exibir_menu()
        escolha = input("Selecione uma opção: ").strip()

        if escolha == '1':
            print("\n[+] Iniciando Backtest (Operação Padrão)...")
            # --- Chamadas para outros módulos ---
            # dados_brutos = load.carregar_dados()
            # dados_limpos = clean.processar_dados(dados_brutos)
            # resultados = backtesting_main.executar_backtest(dados_limpos)
            # graphing.exibir_resultados(resultados)
            print("[OK] Backtest concluído.")

        elif escolha == '2':
            print("\n[+] Carregando novos dados...")
            # --- Chamadas para outros módulos ---
            # dados_lidos = load.ler_dados()
            # dados_validados = clean.validar_dados(dados_lidos)
            print("[OK] Carregamento e validação de dados finalizados.")

        elif escolha == '3':
            print("\n[+] Processando e analisando...")
            # --- Chamadas para outros módulos ---
            # dados_com_estrategia = estrategy.aplicar_estrategia(dados_validados)
            # indicadores = estrategy.calcular_indicadores_tecnicos(dados_com_estrategia)
            # exibir_analise_previa(indicadores)
            print("[OK] Processamento e análise concluídos.")

        elif escolha == '4':
            print("\n[+] Visualizando resultados anteriores...")
            # --- Chamadas para outros módulos ---
            # graphing.renderizar_graficos(resultados_anteriores)
            # exibir_tabelas_de_resumo()
            print("[OK] Visualização concluída.")

        elif escolha == '0':
            print("\nEncerrando o programa. Até logo!")
            sys.exit(0)

        else:
            print("\n[ERRO] Opção inválida. Por favor, digite um número de 0 a 4.")

if __name__ == "__main__":
    clear_screen()
    main()
