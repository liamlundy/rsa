from rsa.rsa import *


def test_encrypt_decrypt():
    pub, priv, mod = get_keys()
    byte_string = b'abcderfg12345678'
    assert decrypt(encrypt(byte_string, priv, mod), pub, mod) == byte_string


def test_sign_message():
    pub, priv, mod = get_keys()
    byte_string = b'abcderfg12345678'
    signed = sign_message(byte_string, priv, mod)
    assert verify_signature(signed, pub, mod)


def test_key_generation():
    pub, priv, mod = get_keys()
    assert pow(pow(7, priv, mod), pub, mod) == 7


def test_encrypt_decrypt_with_large_keys():
    pub, priv, mod = get_keys(2 ** 1023, 2 ** 1024)
    byte_string = b'abcderfg12345678'
    assert decrypt(encrypt(byte_string, priv, mod), pub, mod) == byte_string
