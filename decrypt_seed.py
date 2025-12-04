import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def decrypt_seed(encrypted_seed_b64: str, private_key):
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP-SHA256.
    Returns: 64-character hex seed string.
    """

    # 1. Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. RSA OAEP decrypt
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Convert bytes → UTF-8 string
    hex_seed = decrypted.decode("utf-8").strip()

    # 4. Validate seed
    if len(hex_seed) != 64:
        raise ValueError("Seed must be 64 hex characters")

    if not all(c in "0123456789abcdef" for c in hex_seed.lower()):
        raise ValueError("Invalid hex seed")

    return hex_seed
