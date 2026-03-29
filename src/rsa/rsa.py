import hashlib
from math import gcd
from typing import Tuple

from .utils.codecs import bytes_to_int, int_to_bytes
from .utils.modular_arithmatic import mod_inv
from .utils.rabin_miller import choose_prime


def generate_keys(*, e: int = 65537, key_size: int = 2048) -> Tuple[int, int, int]:
    """
    Generate a public and private key pair for RSA encryption. The public key consists
    of the exponent 'e' and modulus 'n', while the private key consists of the exponent
    'd' and modulus 'n'. The function generates two large prime numbers 'p' and 'q',
    calculates 'n' as their product.

    Args:
        e (int, optional): The public exponent. Defaults to 65537, which is a common
            choice for RSA.
        key_size (int, optional): The desired key size in bits. Defaults to 2048.
    Returns:
        Tuple[int, int, int]: A tuple containing the public exponent 'e', private
            exponent 'd', and modulus 'n'.
    """
    p = choose_prime(key_size // 2)
    q = choose_prime(key_size // 2)
    n = p * q

    # For two primes p and q, the totient φ(n) is (p - 1)(q - 1)
    totient = (p - 1) * (q - 1)

    d = mod_inv(e, totient)

    assert (d * e) % totient == 1

    return e, d, n


def encrypt_value(plain_text: int, key: int, n: int) -> int:
    """
    Encrypt a chunk of plaintext using the RSA encryption algorithm. The plaintext is
    raised to the power of the key and then taken modulo n. The plaintext must be less
    than n and relatively prime to n for the encryption to work correctly.

    Args:
        plain_text (int): The plaintext chunk to be encrypted, represented as an
            integer.
        key (int): The encryption key (public exponent).
        n (int): The modulus used for encryption.
    Returns:
        int: The encrypted ciphertext chunk, represented as an integer.
    """
    # must be hex message
    # error check this -  try/catch
    assert plain_text < n
    assert gcd(plain_text, n) == 1
    return pow(plain_text, key, n)


def decrypt_value(cipher_text: int, key: int, n: int) -> int:
    """
    Decrypt a chunk of ciphertext using the RSA decryption algorithm. The ciphertext is
    raised to the power of the key and then taken modulo n.

    Args:
        cipher_text (int): The ciphertext chunk to be decrypted, represented as an
            integer.
        key (int): The decryption key (private exponent).
        n (int): The modulus used for decryption.
    Returns:
        int: The decrypted plaintext chunk, represented as an integer.
    """
    return pow(cipher_text, key, n)


def encrypt_chunk(chunk: bytes, key: int, n: int) -> bytes:
    value = bytes_to_int(chunk)
    encrypted_value = encrypt_value(value, key, n)
    return int_to_bytes(encrypted_value)


def decrypt_chunk(chunk: bytes, key: int, n: int) -> bytes:
    value = bytes_to_int(chunk)
    decrypted_value = decrypt_value(value, key, n)
    return int_to_bytes(decrypted_value)


def encrypt_bytes(
    plain_bytes: bytes, key: int, n: int, chunk_size: int = None
) -> bytes:
    """
    Takes a byte string and encrypts it in chunks of bytes of length 'chunk_size' with
    key 'key' and modulus 'n'.

    Args:
        plain_bytes (bytes): The plaintext message to be encrypted, represented as a
            byte string.
        key (int): The encryption key (public exponent).
        n (int): The modulus used for encryption.
        chunk_size (int, optional): The size of each chunk in bytes. Defaults to 8.
    Returns:
        bytes: A byte string representing the encrypted message.
    """
    # TODO: Padding
    chunk_size = (n.bit_length() + 7) // 8

    encrypted = b""
    for i in range(0, len(plain_bytes), chunk_size):
        chunk = plain_bytes[i : i + chunk_size]
        encrypted_chunk = encrypt_chunk(chunk, key, n)
        encrypted += encrypted_chunk
    return encrypted


def decrypt_bytes(
    encrypted_bytes: bytes, key: int, n: int, chunk_size: int = None
) -> bytes:
    """Takes a byte string representing encrypted chunks and decrypts them with
    key 'key' and modulus 'n'. The decrypted chunks are concatenated together to form
    the final decrypted byte string.

     Args:
        encrypted_bytes (bytes): A byte string representing the encrypted message.
        key (int): The decryption key (private exponent).
        n (int): The modulus used for decryption.
    Returns:
        bytes: The final decrypted message, represented as a byte string.
    """

    chunk_size = (n.bit_length() + 7) // 8
    print(f"Chunk size: {chunk_size}")

    decrypted = b""
    for i in range(0, len(encrypted_bytes), chunk_size):
        encrypted_chunk = encrypted_bytes[i : i + chunk_size]
        decrypted_chunk = decrypt_chunk(encrypted_chunk, key, n)
        decrypted += decrypted_chunk
    return decrypted


# FIXME needs to be fixed. can't append bytes to list
def sign_message(message: bytes, key: int, n: int) -> bytes:
    """
    Sign a message using the RSA signing algorithm. The message is hashed using MD5, and
    the resulting hash is encrypted with the private key to create the signature. The
    final output is the original message concatenated with the signature. The signature
    can be verified by decrypting it with the public key and comparing the resulting
    hash to a newly computed hash of the original message.

    Args:
        message (bytes): The message to be signed, represented as a byte string.
        key (int): The signing key (private exponent).
        n (int): The modulus used for signing.
    Returns:
        bytes: The original message concatenated with the signature, represented as a
        byte string.
    """
    hashed_message = hashlib.md5(message).digest()
    signature = encrypt_bytes(hashed_message, key, n)
    return message + b"".join(signature)
