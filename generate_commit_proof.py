#!/usr/bin/env python3

import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

# -----------------------------
# Step 1: Get latest commit hash
# -----------------------------
commit_hash = subprocess.check_output(
    ["git", "log", "-1", "--format=%H"]
).decode().strip()
print(f"Commit Hash: {commit_hash}")

# -----------------------------
# Step 2: Load student private key
# -----------------------------
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# -----------------------------
# Step 3: Sign commit hash (RSA-PSS-SHA256)
# -----------------------------
def sign_message(message: str, private_key: rsa.RSAPrivateKey) -> bytes:
    message_bytes = message.encode("utf-8")
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

signature_bytes = sign_message(commit_hash, private_key)

# -----------------------------
# Step 4: Load instructor public key
# -----------------------------
with open("instructor_public.pem", "rb") as f:
    instructor_pub = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

# -----------------------------
# Step 5: Encrypt signature with instructor public key (RSA-OAEP-SHA256)
# -----------------------------
def encrypt_with_public_key(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

encrypted_signature = encrypt_with_public_key(signature_bytes, instructor_pub)

# -----------------------------
# Step 6: Base64 encode encrypted signature
# -----------------------------
encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode("utf-8")
print(f"Encrypted Commit Signature (Base64):\n{encrypted_signature_b64}")
