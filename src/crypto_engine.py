import hashlib
import os

def _expand_key(password, salt, length):
    """Expand password into long key stream"""
    key = hashlib.sha256((password + salt).encode()).digest()

    stream = bytearray()
    while len(stream) < length:
        key = hashlib.sha256(key + password.encode()).digest()
        stream.extend(key)

    return stream[:length]


def encrypt(data: bytes, password: str) -> bytes:
    salt = os.urandom(8).hex()
    key_stream = _expand_key(password, salt, len(data))

    encrypted = bytes([b ^ k for b, k in zip(data, key_stream)])

    # store salt at start
    return salt.encode() + b"::" + encrypted


def decrypt(data: bytes, password: str) -> bytes:
    try:
        salt, encrypted = data.split(b"::", 1)
        salt = salt.decode()
    except:
        raise ValueError("Invalid file format")

    key_stream = _expand_key(password, salt, len(encrypted))

    return bytes([b ^ k for b, k in zip(encrypted, key_stream)])