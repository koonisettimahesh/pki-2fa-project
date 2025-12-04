#!/usr/bin/env python3
import sys
sys.path.insert(0, "/app")
import time
from totp import generate_totp_code

try:
    with open("/app/data/seed.txt", "r") as f:
        hex_seed = f.read().strip()
except FileNotFoundError:
    print("Seed not found")
    exit(1)

# Generate TOTP code
code = generate_totp_code(hex_seed)

# Get UTC timestamp
timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

# Log output
print(f"{timestamp} - 2FA Code: {code}")
