"""
Ponto de Entrada Principal do Sistema de Backtesting de Estratégias de Negociação

RESPONSABILIDADES:
- Inicializar o programa
- Importar e chamar o módulo de interface (interface.py)
- Manter a simplicidade (máximo 20 linhas de código)
- Garantir que o controle seja transferido para os módulos apropriados

FLUXO DE EXECUÇÃO:
1. Executa quando o programa é iniciado
2. Importa o módulo de interface (code.interface.interface)
3. Chama a função principal de interface para exibir menu
4. Aguarda e processa as escolhas do usuário

DEPENDÊNCIAS:
- code.interface.interface (módulo de interface com usuário)

SAÍDA:
- Controle transferido para a interface que roteia para outros módulos

NOTAS:
- Este arquivo deve ser mantido limpo e simples
- Toda a lógica de negócio deve estar em outros módulos
- A interface é responsável por rotear para funcionalidades específicas
"""
from src.interface.interface import main

main()