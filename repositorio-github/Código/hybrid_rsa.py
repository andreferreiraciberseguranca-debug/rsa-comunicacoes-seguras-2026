# hybrid_rsa.py - Esquema híbrido RSA (OAEP/PSS) + AES-256-GCM
# Metodologia alinhada com o artigo IEEE:
# - Mede o ciclo COMPLETO por iteração (inclui verificação e decifra no recetor).
# - Inclui geração de chaves como "pior caso" (em produção seria provisionado offline, p.ex. HSM).
# - AES-256-GCM com nonce 96-bit e AAD (dados associados).

import os
import time
import statistics
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MENSAGEM = b"""ORDEM OPERACIONAL CONFIDENCIAL
ID: OP-2025-178
De: PCGNR-Porto
Para: Brigada Trafico A23
Coordenadas: 39.603178, -7.909292
Hora: 2025-12-15 23:45
Prioridade: ALFA"""

# AAD (metadados/cabeçalho) — autenticado mas não cifrado
AAD = b"header:v1|proto:hybrid|class:confidential"

def medir_rsa(tamanho: int = 2048, iteracoes: int = 1000):
    tempos_ms = []

    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()

        # 1) Keygen (pior caso)
        # Chave do recetor (OAEP) e chave do emissor (PSS)
        priv_recetor = rsa.generate_private_key(public_exponent=65537, key_size=tamanho)
        pub_recetor = priv_recetor.public_key()

        priv_emissor = rsa.generate_private_key(public_exponent=65537, key_size=tamanho)
        pub_emissor = priv_emissor.public_key()

        # 2) Gerar chave de sessão e nonce (AES-256-GCM)
        k_sessao = os.urandom(32)      # 256-bit
        nonce = os.urandom(12)         # 96-bit (recomendado)
        aesgcm = AESGCM(k_sessao)

        # 3) Cifrar (GCM devolve ciphertext || tag)
        c = aesgcm.encrypt(nonce, MENSAGEM, AAD)

        # 4) Encapsular chave de sessão (RSA-OAEP)
        c_k = pub_recetor.encrypt(
            k_sessao,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 5) Assinar elementos críticos (RSA-PSS) — assina AAD||Ck||nonce||C
        to_sign = AAD + c_k + nonce + c
        assinatura = priv_emissor.sign(
            to_sign,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # -------- Lado recetor (verificação + decapsular + decifrar) --------

        # 6) Verificar assinatura
        pub_emissor.verify(
            assinatura,
            to_sign,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # 7) Decapsular chave de sessão
        k_rec = priv_recetor.decrypt(
            c_k,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 8) Decifrar e autenticar (GCM valida tag)
        aesgcm_rec = AESGCM(k_rec)
        m_rec = aesgcm_rec.decrypt(nonce, c, AAD)

        # sanity check
        if m_rec != MENSAGEM:
            raise RuntimeError("Erro: mensagem recuperada não coincide com a original.")

        fim = time.perf_counter_ns()
        tempos_ms.append((fim - inicio) / 1e6)

    desvio = statistics.stdev(tempos_ms) if len(tempos_ms) > 1 else 0.0
    return statistics.mean(tempos_ms), desvio


if __name__ == "__main__":
    media, desvio = medir_rsa(2048, 1000)
    print(f"RSA-{2048} (OAEP/PSS + AES-256-GCM, ciclo completo): {media:.2f} ± {desvio:.2f} ms (N=1000)")
