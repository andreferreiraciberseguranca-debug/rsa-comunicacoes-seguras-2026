# RSA em Comunicações Táticas – ISPGAYA 2025-2026

Repositório do trabalho prático da UC Criptografia Aplicada  
Mestrado em Cibersegurança e Auditoria de Sistemas Informáticos  
Autor: André Filipe Martins Meireles Ferreira (2025107590)

## Objetivo
Avaliação prática do RSA-2048/3072 vs X25519/Ed25519 vs Kyber-768/Dilithium-3 em dispositivos táticos (Raspberry Pi 4, Galaxy A54, Intel i7).

## Conteúdo
- `codigo/` – Implementações híbridas completas
- `dados/` – 30 000 execuções em CSV
- `graficos/` – Figuras usadas no artigo
- `gerar_graficos.py` – Reproduz todos os gráficos

## Como reproduzir
```bash
pip install cryptography liboqs-python pandas matplotlib
python codigo/hybrid_rsa.py
python gerar_graficos.py
