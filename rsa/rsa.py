import hashlib
from math import gcd, ceil, log

from utils.codecs import bytes_to_int, int_to_bytes
from utils.modular_arithmatic import mod_inv
from utils.rabin_miller import choose_prime


def get_keys(min_key_size=2 ** 511, max_key_size=2 ** 512):
    p = choose_prime(min_key_size, max_key_size)
    q = choose_prime(min_key_size, max_key_size)
    n = p*q

    # should be using carmichael?
    totient = (p-1)*(q-1)
    # totient = lcm((p - 1), (q - 1))

    e = 65537

    d = mod_inv(e, totient)

    assert (d*e) % totient == 1

    return e, d, n


def encrypt_chunk(plain_text, key, n):
    # must be hex message
    # error check this -  try/catch
    assert plain_text < n
    assert gcd(plain_text, n) == 1
    return pow(plain_text, key, n)


def decrypt_chunk(cipher_text, key, n):
    return pow(cipher_text, key, n)


def encrypt(plain_bytes, key, n):
    """
    Takes a byte string and encrypts it in chunks of bytes of length 'chunk_size' with key 'key' and modulus 'n'.
    :param plain_bytes: hexadecimal bytes to be encrypted
    :type plain_bytes: bytes
    :param key: key to be used for encryption
    :type key: int
    :param n: modulus to be sued for encryption
    :type n: int
    :return: a byte string of the encrypted input
    :rtype: bytes
    """
    # TODO: Padding
    int_equivalent = bytes_to_int(plain_bytes)
    return int_to_bytes(encrypt_chunk(int_equivalent, key, n))


def decrypt(plain_text, key, n):
    int_equivalent = decrypt_chunk(bytes_to_int(plain_text), key, n)
    return int_to_bytes(int_equivalent)


def sign_message(message, key, n):
    message_hash = hashlib.md5(message).digest()
    signature = encrypt(message_hash, key, n)
    return message + signature


# TODO: Verify this math and figure out how to get signature length
def verify_signature(message_with_signature, key, n):
    # signature_length = ceil(log(key, 16) / 2)
    signature_length = 128  # TODO: Don't hard code this
    signature = message_with_signature[-signature_length:]
    message = message_with_signature[:len(message_with_signature) - signature_length]
    message_hash = hashlib.md5(message).digest()
    return decrypt(signature, key, n) == message_hash
