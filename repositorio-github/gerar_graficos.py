# gerar_graficos.py – Versão melhorada (não corta nomes)
import pandas as pd
import matplotlib.pyplot as plt

# Lê dados
df = pd.read_csv('dados/resultados_rpi4.csv')

# Gráfico de latência
df_group = df.groupby('algoritmo')['tempo_ms'].mean()

plt.figure(figsize=(10, 6))  # Tamanho maior
df_group.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
plt.title('Latência Média – Raspberry Pi 4', fontsize=14, pad=20)
plt.ylabel('Tempo (ms)', fontsize=12)
plt.xlabel('Algoritmo', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Roda os nomes 45° e alinha à direita
plt.tight_layout()  # Evita cortes
plt.grid(axis='y', alpha=0.3)

plt.savefig('Gráficos/grafico_latencia.png', dpi=300, bbox_inches='tight')
print("Gráfico gerado com sucesso!")