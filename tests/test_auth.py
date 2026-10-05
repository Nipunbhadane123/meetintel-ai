import pytest
from storage.auth import hash_password, verify_password

def test_password_hashing():
    pwd = "my_secure_password"
    hashed = hash_password(pwd)
    
    assert verify_password(pwd, hashed) == True
    assert verify_password("wrong_password", hashed) == False
    assert verify_password(pwd, "invalid_hash_format") == False
