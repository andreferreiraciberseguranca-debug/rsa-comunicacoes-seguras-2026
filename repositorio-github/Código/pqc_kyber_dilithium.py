# pqc_kyber_dilithium.py - Pós-quântico (requer liboqs-python)
import oqs
import time
import statistics
import os

def medir_pqc(iteracoes=100):
    tempos = []
    kem = oqs.KeyEncapsulation('Kyber768')
    sig = oqs.Signature('Dilithium3')
    
    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()
        
        # Troca de chaves Kyber-768
        pk_kem, sk_kem = kem.keypair()
        ciphertext_kem, shared_secret = kem.encap_secret(pk_kem)
        
        # Assinatura Dilithium-3
        pk_sig, sk_sig = sig.keypair()
        signature = sig.sign(b"mensagem teste")
        
        fim = time.perf_counter_ns()
        tempos.append((fim - inicio) / 1e6)
    
    return statistics.mean(tempos), statistics.stdev(tempos)

if __name__ == "__main__":
    media, desvio = medir_pqc(100)
    print(f"Kyber-768 + Dilithium-3: {media:.2f} ± {desvio:.2f} ms")