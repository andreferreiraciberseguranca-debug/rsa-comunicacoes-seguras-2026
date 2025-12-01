# hybrid_rsa.py - Esquema híbrido RSA + AES-256-GCM (NIST-recomendado)
import os
import time
import statistics
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Mensagem exemplo realista (ordem operacional PSP/GNR)
mensagem = b"""ORDEM OPERACIONAL CONFIDENCIAL
ID: OP-2025-178
De: PCGNR-Porto
Para: Brigada Trafico A23
Coordenadas: 39.603178, -7.909292
Hora: 2025-12-15 23:45
Prioridade: ALFA"""

def medir_rsa(tamanho=2048, iteracoes=1000):
    tempos = []
    for _ in range(iteracoes):
        inicio = time.perf_counter_ns()
        
        # Geração de chaves RSA (offline em HSM na prática)
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=tamanho)
        public_key = private_key.public_key()
        
        # Assinatura RSA-PSS (não-repúdio)
        signature = private_key.sign(
            mensagem,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        
        # Troca de chave RSA-OAEP
        aes_key = os.urandom(32)  # AES-256
        enc_key = public_key.encrypt(
            aes_key,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        
        # Cifragem AES-256-GCM
        aesgcm = AESGCM(aes_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, mensagem, None)
        
        fim = time.perf_counter_ns()
        tempos.append((fim - inicio) / 1e6)  # Convert to ms
    
    return statistics.mean(tempos), statistics.stdev(tempos)

if __name__ == "__main__":
    media, desvio = medir_rsa(2048, 1000)
    print(f"RSA-2048: {media:.2f} ± {desvio:.2f} ms (1000 iteracoes)")