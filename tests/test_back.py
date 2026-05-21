from dataprocessing.load import load_data
from graphing.graphing import generate_sample_time_series, plot_time_series
import pandas
import matplotlib.pyplot as plt

assert isinstance(load_data(
    indice='^BVSP', 
    fonte='yfinance', 
    tempo='1y', salvar=False), pandas.DataFrame)

assert isinstance(plot_time_series(generate_sample_time_series(length=3), label='Série de Preço', colors=['#d62728'], line_style='-', marker='o'), plt.Axes)
