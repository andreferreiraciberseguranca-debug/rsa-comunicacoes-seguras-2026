# pqc_kyber_dilithium.py - Pós-quântico (ML-KEM-768 + ML-DSA-65 / Dilithium-3)
# Requer: liboqs-python
#
# Metodologia (IEEE):
# - Mede ciclo completo (keygen + encap + decap + sign + verify) por iteração.
# - Inclui keygen como "pior caso" para custo máximo.
# - No artigo, o custo "PQC total" pode ser apresentado como soma/encadeamento dos componentes.

import time
import statistics
import oqs

MENSAGEM_TESTE = b"mensagem teste (benchmark PQC)"

def medir_pqc(iteracoes: int = 1000):
    tempos_ms = []

    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()

        # --- ML-KEM-768 (Kyber-768) ---
        with oqs.KeyEncapsulation("Kyber768") as kem:
            pk_kem, sk_kem = kem.generate_keypair()
            ct_kem, ss_emissor = kem.encap_secret(pk_kem)
            ss_recetor = kem.decap_secret(ct_kem, sk_kem)

            if ss_emissor != ss_recetor:
                raise RuntimeError("Erro: shared secret KEM não coincide (encap/decap).")

        # --- ML-DSA-65 (Dilithium-3) ---
        with oqs.Signature("Dilithium3") as sig:
            pk_sig, sk_sig = sig.generate_keypair()
            assinatura = sig.sign(MENSAGEM_TESTE, sk_sig)
            ok = sig.verify(MENSAGEM_TESTE, assinatura, pk_sig)

            if not ok:
                raise RuntimeError("Erro: verificação de assinatura PQC falhou.")

        fim = time.perf_counter_ns()
        tempos_ms.append((fim - inicio) / 1e6)

    desvio = statistics.stdev(tempos_ms) if len(tempos_ms) > 1 else 0.0
    return statistics.mean(tempos_ms), desvio


if __name__ == "__main__":
    media, desvio = medir_pqc(1000)
    print(f"PQC (Kyber-768 + Dilithium-3, ciclo completo): {media:.2f} ± {desvio:.2f} ms (N=1000)")
