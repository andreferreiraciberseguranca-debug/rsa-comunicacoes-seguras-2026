# gerar_graficos.py - Gera gráficos do artigo
import pandas as pd
import matplotlib.pyplot as plt

# Lê dados
df = pd.read_csv('dados/resultados_rpi4.csv')

# Gráfico de latência
df_group = df.groupby('algoritmo')['tempo_ms'].mean()
df_group.plot(kind='bar')
plt.title('Latência Média - Raspberry Pi 4')
plt.ylabel('Tempo (ms)')
plt.savefig('graficos/grafico_latencia.png')
print("Gráficos gerados!")