# gerar_graficos.py – Geração de gráficos para análise experimental
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'Dados' / 'resultados_rpi4.csv'
OUTPUT_DIR = BASE_DIR / 'Graficos'
OUTPUT_DIR.mkdir(exist_ok=True)

# Ler dados
df = pd.read_csv(DATA_FILE)

# Agregação
df_group = df.groupby('algoritmo')['tempo_ms'].mean()

# Gráfico
plt.figure(figsize=(10, 6))
df_group.plot(kind='bar')
plt.title('Latência Média – Raspberry Pi 4')
plt.ylabel('Tempo (ms)')
plt.xlabel('Algoritmo')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Guardar
plt.savefig(OUTPUT_DIR / 'grafico_latencia.png', dpi=300)
plt.close()

print("Gráfico gerado com sucesso.")
