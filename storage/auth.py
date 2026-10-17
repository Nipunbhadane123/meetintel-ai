import hashlib
import os
import secrets
from typing import Optional

# Configuration
SALT_SIZE = 16
HASH_ITERATIONS = 100000

def hash_password(password: str) -> str:
    """Hashes a password with a random salt using PBKDF2 HMAC SHA-256."""
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string.")
    salt = secrets.token_bytes(SALT_SIZE)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, HASH_ITERATIONS)
    # Store as salt:hash
    return f"{salt.hex()}:{pwd_hash.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hash with constant-time comparison."""
    if not plain_password or not hashed_password:
        return False
    if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
        return False
    try:
        parts = hashed_password.split(':')
        if len(parts) != 2:
            return False
        salt_hex, hash_hex = parts
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        
        pwd_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, HASH_ITERATIONS)
        return secrets.compare_digest(pwd_hash, expected_hash)
    except Exception:
        return False
