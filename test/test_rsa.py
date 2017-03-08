from rsa import *


def test_encrypt_decrypt():
    pub, priv, mod = get_keys()
    byte_string = b'abcderfg12345678'
    assert decrypt(encrypt(byte_string, priv, mod), pub, mod) == byte_string


def test_key_generation():
    pub, priv, mod = get_keys()
    assert pow(pow(7, priv, mod), pub, mod) == 7
