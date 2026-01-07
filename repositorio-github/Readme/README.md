RSA em Comunicações Seguras para Forças de Segurança – ISPGAYA 2025–2026

Repositório do trabalho prático de Criptografia Aplicada.
Autor: André Filipe Martins Meireles Ferreira (Nº 2025107590)
Mestrado em Cibersegurança e Auditoria de Sistemas Informáticos.

Objetivo
Implementação e benchmark experimental do esquema híbrido RSA + AES-256-GCM,
comparado com alternativas modernas e pós-quânticas
(X25519/Ed25519, Kyber-768/Dilithium-3),
em dispositivos representativos de cenários operacionais
(Raspberry Pi 4, Galaxy A54, Intel i7).

Conteúdo
codigo/: Scripts Python para implementação e benchmark criptográfico.
dados/: Resultados experimentais (CSV) contendo tempos (ms) e consumo energético (mAh).
graficos/: Figuras para o artigo (latência, comparação de algoritmos).
gerar_graficos.py: Script para geração automática de gráficos.

Como Reproduzir
1. Clonar o repositório:
   git clone https://github.com/andreferreiraciberseguranca-debug/rsa-comunicacoes-seguras-2026.git
2. Instalar dependências:
   pip install cryptography liboqs-python pandas matplotlib
3. Executar benchmarks:
   python codigo/hybrid_rsa.py
4. Gerar gráficos:
   python gerar_graficos.py

Notas Metodológicas
Os resultados apresentados baseiam-se em medições reais realizadas em hardware físico,
com múltiplas iterações por algoritmo, de forma a mitigar variabilidade estatística.

Licença
MIT License – uso académico e científico.
