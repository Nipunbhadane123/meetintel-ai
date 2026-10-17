import os
import base64
import hashlib
from cryptography.fernet import Fernet

def _get_fernet_key() -> bytes:
    raw_secret = os.getenv("SECRET_KEY", "meetintel-enterprise-secret-key-2026")
    # Derive 32-byte urlsafe base64 key
    digest = hashlib.sha256(raw_secret.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_token(plain_token: str) -> str:
    """Encrypts an OAuth access/refresh token or secret."""
    if not plain_token:
        return ""
    f = Fernet(_get_fernet_key())
    return f.encrypt(plain_token.encode('utf-8')).decode('utf-8')

def decrypt_token(encrypted_token: str) -> str:
    """Decrypts an encrypted token."""
    if not encrypted_token:
        return ""
    try:
        f = Fernet(_get_fernet_key())
        return f.decrypt(encrypted_token.encode('utf-8')).decode('utf-8')
    except Exception:
        # Return empty string if decryption fails rather than leaking raw ciphertext
        return ""
