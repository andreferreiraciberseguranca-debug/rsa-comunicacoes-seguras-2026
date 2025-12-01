# pqc_kyber_dilithium.py
# Só funciona se tiveres liboqs-python instalado
import oqs, time, statistics

def medir_pqc(iteracoes=1000):
    tempos = []
    kem = oqs.KeyEncapsulation('Kyber768')
    sig = oqs.Signature('Dilithium3')
    
    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()
        
        pk_kem, sk_kem = kem.keypair()
        ciphertext, shared_secret = kem.encap_secret(pk_kem)
        
        pk_sig, sk_sig = sig.keypair()
        signature = sig.sign(b"mensagem teste")
        
        fim = time.perf_counter_ns()
        tempos.append((fim - inicio) / 1e6)
    
    return statistics.mean(tempos)

if __name__ == "__main__":
    print(f"Kyber768+Dilithium3 médio: {medir_pqc(100):.2f} ms")
