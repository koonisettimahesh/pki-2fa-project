import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def decrypt_seed():
    # 1. Read encrypted seed
    with open("encrypted_seed.txt", "r") as f:
        encrypted_base64 = f.read().strip()

    encrypted_bytes = base64.b64decode(encrypted_base64)

    # 2. Load private key
    with open("student_private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # 3. Decrypt using RSA-OAEP-SHA256
    decrypted_seed = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 4. Save plaintext seed
    with open("seed.txt", "wb") as f:
        f.write(decrypted_seed)

    print("Decryption complete. Seed saved to seed.txt")

decrypt_seed()
