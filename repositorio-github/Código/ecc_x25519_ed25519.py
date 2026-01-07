# Nota metodológica (IEEE):
# AES-256-GCM é mantido constante no estudo e, por isso, é EXCLUÍDO aqui para isolar
# o custo assimétrico (X25519 para acordo de chave + Ed25519 para assinatura/validação).
# Este ficheiro mede apenas o "custo ECC assimétrico" (handshake + assinatura + verificação).
#
# ecc_x25519_ed25519.py - ECC alternativa ao RSA (custo assimétrico)

import time
import statistics
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

MENSAGEM_TESTE = b"mensagem teste (benchmark ECC)"

def medir_ecc(iteracoes: int = 1000):
    tempos_ms = []

    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()

        # 1) Acordo de chave X25519 (duas partes: emissor e recetor)
        priv_a = x25519.X25519PrivateKey.generate()
        priv_b = x25519.X25519PrivateKey.generate()
        pub_a = priv_a.public_key()
        pub_b = priv_b.public_key()

        shared_a = priv_a.exchange(pub_b)
        shared_b = priv_b.exchange(pub_a)

        # 2) Derivação de chave (HKDF) — simula o KDF de handshake
        k_a = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"handshake data"
        ).derive(shared_a)

        k_b = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"handshake data"
        ).derive(shared_b)

        # sanity check: ambos devem derivar a mesma chave
        if k_a != k_b:
            raise RuntimeError("Erro: HKDF derivou chaves diferentes (handshake inválido).")

        # 3) Assinatura + verificação Ed25519 (inclui lado recetor)
        priv_sig = ed25519.Ed25519PrivateKey.generate()
        pub_sig = priv_sig.public_key()
        assinatura = priv_sig.sign(MENSAGEM_TESTE)
        pub_sig.verify(assinatura, MENSAGEM_TESTE)

        fim = time.perf_counter_ns()
        tempos_ms.append((fim - inicio) / 1e6)

    # stdev exige >=2 amostras
    desvio = statistics.stdev(tempos_ms) if len(tempos_ms) > 1 else 0.0
    return statistics.mean(tempos_ms), desvio


if __name__ == "__main__":
    media, desvio = medir_ecc(1000)
    print(f"ECC (X25519+Ed25519, assimétrico): {media:.2f} ± {desvio:.2f} ms (N=1000)")
