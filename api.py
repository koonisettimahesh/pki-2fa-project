from fastapi import FastAPI, HTTPException
import base64
from decrypt_seed import decrypt_seed
from totp import generate_totp_code, verify_totp_code
from pathlib import Path
import time

app = FastAPI()

SEED_FILE = Path("/data/seed.txt")  # MUST exist only inside container


@app.post("/decrypt-seed")
def decrypt_seed_endpoint(payload: dict):
    try:
        encrypted_seed = payload.get("encrypted_seed")
        if not encrypted_seed:
            raise Exception("Missing encrypted seed")

        # Load private key
        from cryptography.hazmat.primitives import serialization
        with open("student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        # Decrypt
        decrypted_hex = decrypt_seed(encrypted_seed, private_key)

        # Ensure /data exists
        SEED_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Save seed
        SEED_FILE.write_text(decrypted_hex)

        return {"status": "ok"}

    except Exception as e:
        print("Decryption error:", e)
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = SEED_FILE.read_text().strip()

    code = generate_totp_code(hex_seed)
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(payload: dict):
    code = payload.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = SEED_FILE.read_text().strip()

    valid = verify_totp_code(hex_seed, code)

    return {"valid": valid}
