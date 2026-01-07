# Nota: AES-GCM excluído para isolar custo ECC assimétrico
# ecc_x25519_ed25519.py - ECC alternativa ao RSA
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os, time, statistics

def medir_ecc(iteracoes=1000):
    tempos = []
    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()
        
        # Troca de chaves X25519
        priv_x = x25519.X25519PrivateKey.generate()
        pub_x = priv_x.public_key()
        shared_key = priv_x.exchange(pub_x)
        aes_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data').derive(shared_key)
        
        # Assinatura Ed25519
        priv_ed = ed25519.Ed25519PrivateKey.generate()
        signature = priv_ed.sign(b"mensagem teste")
        
        fim = time.perf_counter_ns()
        tempos.append((fim - inicio) / 1e6)
    
    return statistics.mean(tempos), statistics.stdev(tempos)

if __name__ == "__main__":
    media, desvio = medir_ecc(1000)

    print(f"ECC (X25519+Ed25519): {media:.2f} ± {desvio:.2f} ms")
