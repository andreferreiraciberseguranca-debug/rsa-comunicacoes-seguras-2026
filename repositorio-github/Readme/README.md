# RSA em Comunicações Seguras para Forças de Segurança – ISPGAYA 2025-2026

Repositório do trabalho prático de Criptografia Aplicada.  
Autor: André Filipe Martins Meireles Ferreira (Nº 2025107590)  
Mestrado em Cibersegurança e Auditoria de Sistemas Informáticos.

## Objetivo
Implementação e benchmark do esquema híbrido RSA + AES-256-GCM vs alternativas (X25519/Ed25519, Kyber-768/Dilithium-3) em dispositivos representativos (Raspberry Pi 4, Galaxy A54, Intel i7).

## Conteúdo
- **codigo/**: Scripts Python para esquemas híbridos.
- **dados/**: CSVs com 30 000 execuções (tempos em ms, consumo em mAh).
- **graficos/**: Figuras para o artigo (fluxograma, latência, evolução de chaves).
- **gerar_graficos.py**: Gera gráficos automaticamente.

## Como Reproduzir
1. Clona o repo: `git clone https://github.com/andreferreiraciberseguranca-debug/rsa-comunicacoes-seguras-2026.git`
2. Instala dependências: `pip install cryptography liboqs-python pandas matplotlib`
3. Corre testes: `python codigo/hybrid_rsa.py`
4. Gera gráficos: `python gerar_graficos.py`

Dados baseados em testes reais em hardware tático (dezembro 2025).  
Licença: MIT para uso académico.