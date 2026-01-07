# gerar_graficos.py — gera gráficos de latência média por dispositivo
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DADOS = "repositorio-github/Dados"
BASE_GRAFICOS = "repositorio-github/Gráficos"

MAP = {
    "rpi4": "resultados_rpi4.csv",
    "i7": "resultados_i7.csv",
    "galaxy": "resultados_galaxy.csv",
}

os.makedirs(BASE_GRAFICOS, exist_ok=True)

for dev, fname in MAP.items():
    path = os.path.join(BASE_DADOS, fname)
    df = pd.read_csv(path)

    g = df.groupby("algoritmo")["tempo_ms"].mean().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    g.plot(kind="bar")
    plt.title(f"Latência média por algoritmo — {dev}")
    plt.ylabel("Tempo (ms)")
    plt.xlabel("Algoritmo")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    out = os.path.join(BASE_GRAFICOS, f"grafico_latencia_{dev}.png")
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()

print("Gráficos gerados com sucesso.")
