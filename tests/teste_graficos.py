import pandas as pd
import matplotlib.pyplot as plt

from graphing.graphing import (
    plot_equity_curve, 
    plot_drawdown,
    plot_cumulative_returns,
    plot_volatility,
    generate_sample_time_series,
    plot_bollinger_bands_chart,
    plot_rsi_chart,
    generate_performance_summary
)

def rodar_testes_visuais():
    print("Iniciando bateria COMPLETA de testes institucionais...\n")

    # --- 1. A NOSSA MASSA DE DADOS ---
    # Histórico de Conta
    historico_falso = [
        {'date': pd.Timestamp('2026-01-01'), 'cash': 10000.0, 'portfolio_value': 10000.0},
        {'date': pd.Timestamp('2026-01-02'), 'cash': 5000.0,  'portfolio_value': 10200.0},
        {'date': pd.Timestamp('2026-01-03'), 'cash': 5000.0,  'portfolio_value': 9800.0},
        {'date': pd.Timestamp('2026-01-04'), 'cash': 5000.0,  'portfolio_value': 11500.0},
        {'date': pd.Timestamp('2026-01-05'), 'cash': 11450.0, 'portfolio_value': 11450.0},
    ]

    # Histórico de Trades (NOVO!) - Simula 3 vitórias e 1 derrota pesada
    trades_falsos = [
        {'symbol': 'VALE3', 'entry_date': '2026-01-01', 'exit_date': '2026-01-02', 'profit': 200.0},  # Gain
        {'symbol': 'PETR4', 'entry_date': '2026-01-02', 'exit_date': '2026-01-03', 'profit': -400.0}, # Loss
        {'symbol': 'ITUB4', 'entry_date': '2026-01-03', 'exit_date': '2026-01-04', 'profit': 1700.0}, # Super Gain
        {'symbol': 'BBDC4', 'entry_date': '2026-01-04', 'exit_date': '2026-01-05', 'profit': -50.0},  # Pequeno Loss
    ]

    serie_precos_longa = generate_sample_time_series(length=60)

    # --- 2. GERAÇÃO DOS GRÁFICOS (Renderiza silenciosamente e salva) ---
    print("Gerando e salvando 6 painéis de gráficos em PNG...")
    plot_equity_curve(historico_falso)
    plt.savefig('teste_patrimonio.png', bbox_inches='tight', dpi=300); plt.close()

    plot_drawdown(historico_falso)
    plt.savefig('teste_drawdown.png', bbox_inches='tight', dpi=300); plt.close()

    plot_cumulative_returns(serie_precos_longa)
    plt.savefig('teste_retorno_acumulado.png', bbox_inches='tight', dpi=300); plt.close()

    plot_volatility(serie_precos_longa, window=10)
    plt.savefig('teste_volatilidade.png', bbox_inches='tight', dpi=300); plt.close()

    plot_bollinger_bands_chart(serie_precos_longa)
    plt.savefig('teste_bollinger.png', bbox_inches='tight', dpi=300); plt.close()

    plot_rsi_chart(serie_precos_longa)
    plt.savefig('teste_rsi.png', bbox_inches='tight', dpi=300); plt.close()

    # --- 3. A TABELA FINAL DE PERFORMANCE ---
    print("\nCalculando a Matemática do Backtest...")
    
    # Passamos as DUAS listas agora!
    tabela_final = generate_performance_summary(historico_falso, trades_falsos)
    
    print("\n" + "="*55)
    print(" EXTRATO OFICIAL DO BACKTEST ".center(55))
    print("="*55)
    print(tabela_final)
    print("="*55)

    print("\n✅ Sucesso! 6 Gráficos gerados e tabela completa exibida.")

if __name__ == '__main__':
    rodar_testes_visuais()