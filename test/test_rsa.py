from rsa.rsa import decrypt_bytes, encrypt_bytes, generate_keys


def test_encrypt_decrypt():
    pub, priv, mod = generate_keys()
    byte_string = b"abcderfg12345678"
    encrypted = encrypt_bytes(byte_string, priv, mod, chunk_size=64)
    decrypted = decrypt_bytes(encrypted, pub, mod)
    assert decrypted == byte_string


def test_encrypt_decrypt_string():
    pub, priv, mod = generate_keys()
    byte_string = "abcderfg12345678"
    encrypted = encrypt_bytes(byte_string.encode(), priv, mod)
    decrypted = decrypt_bytes(encrypted, pub, mod).decode()
    assert decrypted == byte_string


def test_key_generation():
    pub, priv, mod = generate_keys()
    assert pow(pow(7, priv, mod), pub, mod) == 7
