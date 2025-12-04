import base64
import binascii
import pyotp


def _hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex seed to base32 string.
    """
    # 1. hex → bytes
    seed_bytes = binascii.unhexlify(hex_seed)

    # 2. bytes → base32
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code from hex seed.
    """
    # Convert hex to base32
    base32_seed = _hex_to_base32(hex_seed)

    # Create TOTP object
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # Generate current code
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a TOTP code with ± valid_window tolerance.
    """
    # Convert hex to base32
    base32_seed = _hex_to_base32(hex_seed)

    # Create TOTP object
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # Verify with time window
    return totp.verify(code, valid_window=valid_window)
