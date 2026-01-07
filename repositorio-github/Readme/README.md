RSA em Comunicações Seguras para Forças de Segurança – ISPGAYA 2025-2026

Repositório do trabalho prático de Criptografia Aplicada.
Autor: André Filipe Martins Meireles Ferreira (Nº 2025107590)
Mestrado em Cibersegurança e Auditoria de Sistemas Informáticos.

------------------------------------------------------------

Objetivo

Implementação e avaliação experimental (benchmark) do esquema híbrido
RSA + AES-256-GCM e comparação com alternativas modernas:
X25519/Ed25519 (ECC) e Kyber-768/Dilithium-3 (PQC).

Os testes são realizados em dispositivos representativos de contextos
operacionais distintos:
- Raspberry Pi 4 (dispositivo de baixa potência)
- Samsung Galaxy A54 (plataforma móvel)
- Intel Core i7 (posto de comando / backend)

------------------------------------------------------------

Conteúdo do Repositório

Código/
- Scripts Python para medição de latência criptográfica:
  - hybrid_rsa.py (RSA-OAEP + RSA-PSS + AES-256-GCM)
  - ecc_x25519_ed25519.py (X25519 + Ed25519)
  - pqc_kyber_dilithium.py (Kyber-768 + Dilithium-3)

Dados/
- Ficheiros CSV com resultados experimentais (latência em ms).
- Os datasets completos resultam da agregação de múltiplas execuções
  (até 30 000 operações no total), conforme descrito no artigo IEEE.

Gráficos/
- Figuras utilizadas no artigo científico (fluxograma do esquema híbrido,
  gráficos de latência por algoritmo e dispositivo).

gerar_graficos.py
- Script auxiliar para gerar automaticamente gráficos a partir dos CSVs.

------------------------------------------------------------

Metodologia de Medição

- RSA:
  A latência inclui geração de chaves, assinatura RSA-PSS,
  encapsulamento RSA-OAEP e cifra simétrica AES-256-GCM.
  Esta opção representa um cenário conservador (pior caso / cold start),
  relevante para análise de viabilidade operacional.

- ECC (X25519/Ed25519) e PQC (Kyber/Dilithium):
  A latência inclui handshake criptográfico e assinatura digital.
  Em algumas execuções, a cifra simétrica AES-GCM é incluída
  para permitir comparação end-to-end com o esquema híbrido RSA.

- As medições de tempo utilizam time.perf_counter_ns().

------------------------------------------------------------

Medição Energética

Os valores de consumo energético (mAh), quando apresentados,
foram obtidos através de medições externas ao código Python,
utilizando ferramentas específicas por plataforma
(ex.: monitorização de energia em Raspberry Pi e Android).

------------------------------------------------------------

Como Reproduzir

1. Clonar o repositório:
   git clone https://github.com/andreferreiraciberseguranca-debug/rsa-comunicacoes-seguras-2026.git

2. Instalar dependências:
   pip install cryptography liboqs-python pandas matplotlib

3. Executar testes (exemplo RSA):
   python Código/hybrid_rsa.py

4. Gerar gráficos:
   python gerar_graficos.py

------------------------------------------------------------

Notas Finais

- Os resultados experimentais baseiam-se em testes reais realizados
  em hardware físico (dezembro de 2025).
- Este repositório suporta e complementa o artigo científico
  submetido em formato IEEE.

Licença: MIT (uso académico).
