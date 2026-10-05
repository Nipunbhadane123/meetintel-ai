import hashlib
import os
import secrets
from typing import Optional

# Configuration
SALT_SIZE = 16
HASH_ITERATIONS = 100000

def hash_password(password: str) -> str:
    """Hashes a password with a random salt."""
    salt = secrets.token_bytes(SALT_SIZE)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, HASH_ITERATIONS)
    # Store as salt:hash
    return f"{salt.hex()}:{pwd_hash.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hash."""
    try:
        salt_hex, hash_hex = hashed_password.split(':')
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        
        pwd_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, HASH_ITERATIONS)
        return secrets.compare_digest(pwd_hash, expected_hash)
    except ValueError:
        return False
