import hashlib
from math import gcd

from utils.codecs import bytes_to_int, int_to_bytes
from utils.modular_arithmatic import mod_inv
from utils.rabin_miller import choose_prime


def get_keys():
    p = choose_prime()
    q = choose_prime()
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


def encrypt(plain_bytes, key, n, chunk_size=8):
    """
    Takes a byte string and encrypts it in chunks of bytes of length 'chunk_size' with key 'key' and modulus 'n'.
    :param plain_bytes: hexadecimal bytes to be encrypted
    :type plain_bytes: bytes
    :param key: key to be used for encryption
    :type key: int
    :param n: modulus to be sued for encryption
    :type n: int
    :param chunk_size: number of bytes to be encrypted at one time
    :type chunk_size: int
    :return: a byte string of the encrypted input
    :rtype: bytes
    """
    # TODO: Padding
    encrypted = []
    for i in range(0, len(plain_bytes), chunk_size):
        chunk = bytes_to_int(plain_bytes[i: i + chunk_size])
        encrypted.append(int_to_bytes(encrypt_chunk(chunk, key, n)))
    return encrypted


def decrypt(plain_text_array, key, n):
    decrypted = b''
    for chunk in plain_text_array:
        decrypted_chunk = decrypt_chunk(bytes_to_int(chunk), key, n)
        decrypted += int_to_bytes(decrypted_chunk)
    return decrypted


# need sto be fixed. cant append bytes to list
def sign_message(message, key, n):
    hashed_message = hashlib.md5(message).digest()
    signature = encrypt(hashed_message, key, n)
    return message + signature

