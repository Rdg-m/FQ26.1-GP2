import pandas as pd
import matplotlib.pyplot as plt

from graphing.graphing import plot_equity_curve, plot_drawdown

def rodar_testes_visuais():
    print("Iniciando bateria de testes de gráficos...\n")

    historico_falso = [
        {'date': pd.Timestamp('2026-01-01'), 'cash': 10000.0, 'portfolio_value': 10000.0},
        {'date': pd.Timestamp('2026-01-02'), 'cash': 5000.0,  'portfolio_value': 10200.0}, # Subiu (Drawdown 0%)
        {'date': pd.Timestamp('2026-01-03'), 'cash': 5000.0,  'portfolio_value': 9800.0},  # Caiu (Drawdown ~3.9%)
        {'date': pd.Timestamp('2026-01-04'), 'cash': 5000.0,  'portfolio_value': 11500.0}, # Novo Pico! (Drawdown 0%)
        {'date': pd.Timestamp('2026-01-05'), 'cash': 11450.0, 'portfolio_value': 11450.0}, # Caiu levemente
    ]

    print("1/2: Gerando Curva de Patrimônio (Equity Curve)...")
    plot_equity_curve(historico_falso)
    plt.savefig('teste_patrimonio.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("  -> Salvo como 'teste_patrimonio.png'")

    print("2/2: Gerando Gráfico de Drawdown (Quedas)...")
    plot_drawdown(historico_falso)
    plt.savefig('teste_drawdown.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("  -> Salvo como 'teste_drawdown.png'")

    print("\n✅ Todos os testes concluídos com sucesso!")

if __name__ == '__main__':
    rodar_testes_visuais()