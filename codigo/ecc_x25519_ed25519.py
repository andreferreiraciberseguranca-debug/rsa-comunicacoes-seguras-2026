# ecc_x25519_ed25519.py
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os, time, statistics

def medir_ecc(iteracoes=1000):
    tempos = []
    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()
        
        priv_x = x25519.X25519PrivateKey.generate()
        pub_x = priv_x.public_key()
        shared = priv_x.exchange(pub_x)
        
        priv_ed = ed25519.Ed25519PrivateKey.generate()
        signature = priv_ed.sign(b"mensagem teste")
        
        fim = time.perf_counter_ns()
        tempos.append((fim - inicio) / 1e6)
    
    return statistics.mean(tempos)

if __name__ == "__main__":
    print(f"ECC médio: {medir_ecc(1000):.2f} ms")
