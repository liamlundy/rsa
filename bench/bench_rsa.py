"""
Benchmarks for the Python RSA implementation.

Run with:
    uv run pytest bench/ --benchmark-only
    uv run pytest bench/ --benchmark-only --benchmark-sort=mean
"""
import pytest
from rsa.rsa import decrypt_bytes, encrypt_bytes, generate_keys
from rsa.utils.rabin_miller import choose_prime, is_prime

# ---------------------------------------------------------------------------
# Shared fixtures: generate keys once per benchmark session at multiple sizes
# ---------------------------------------------------------------------------

SHORT_MESSAGE = b"Hello, RSA benchmark!"
LONG_MESSAGE = b"A" * 4096


@pytest.fixture(scope="session")
def keys_512():
    return generate_keys(key_size=512)


@pytest.fixture(scope="session")
def keys_1024():
    return generate_keys(key_size=1024)


@pytest.fixture(scope="session")
def keys_2048():
    return generate_keys(key_size=2048)


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------


def test_keygen_512(benchmark):
    benchmark(generate_keys, key_size=512)


def test_keygen_1024(benchmark):
    benchmark(generate_keys, key_size=1024)


# ---------------------------------------------------------------------------
# Encryption
# ---------------------------------------------------------------------------


def test_encrypt_short_512(benchmark, keys_512):
    e, d, n = keys_512
    benchmark(encrypt_bytes, SHORT_MESSAGE, e, n)


def test_encrypt_short_1024(benchmark, keys_1024):
    e, d, n = keys_1024
    benchmark(encrypt_bytes, SHORT_MESSAGE, e, n)


def test_encrypt_short_2048(benchmark, keys_2048):
    e, d, n = keys_2048
    benchmark(encrypt_bytes, SHORT_MESSAGE, e, n)


def test_encrypt_long_512(benchmark, keys_512):
    e, d, n = keys_512
    benchmark(encrypt_bytes, LONG_MESSAGE, e, n)


def test_encrypt_long_1024(benchmark, keys_1024):
    e, d, n = keys_1024
    benchmark(encrypt_bytes, LONG_MESSAGE, e, n)


def test_encrypt_long_2048(benchmark, keys_2048):
    e, d, n = keys_2048
    benchmark(encrypt_bytes, LONG_MESSAGE, e, n)


# ---------------------------------------------------------------------------
# Decryption
# ---------------------------------------------------------------------------


def test_decrypt_short_512(benchmark, keys_512):
    e, d, n = keys_512
    encrypted = encrypt_bytes(SHORT_MESSAGE, e, n)
    benchmark(decrypt_bytes, encrypted, d, n)


def test_decrypt_short_1024(benchmark, keys_1024):
    e, d, n = keys_1024
    encrypted = encrypt_bytes(SHORT_MESSAGE, e, n)
    benchmark(decrypt_bytes, encrypted, d, n)


def test_decrypt_short_2048(benchmark, keys_2048):
    e, d, n = keys_2048
    encrypted = encrypt_bytes(SHORT_MESSAGE, e, n)
    benchmark(decrypt_bytes, encrypted, d, n)


def test_decrypt_long_512(benchmark, keys_512):
    e, d, n = keys_512
    encrypted = encrypt_bytes(LONG_MESSAGE, e, n)
    benchmark(decrypt_bytes, encrypted, d, n)


def test_decrypt_long_1024(benchmark, keys_1024):
    e, d, n = keys_1024
    encrypted = encrypt_bytes(LONG_MESSAGE, e, n)
    benchmark(decrypt_bytes, encrypted, d, n)


def test_decrypt_long_2048(benchmark, keys_2048):
    e, d, n = keys_2048
    encrypted = encrypt_bytes(LONG_MESSAGE, e, n)
    benchmark(decrypt_bytes, encrypted, d, n)


# ---------------------------------------------------------------------------
# Primality / prime generation
# ---------------------------------------------------------------------------


def test_is_prime_small(benchmark):
    benchmark(is_prime, 104729)  # a known prime


def test_is_prime_large(benchmark):
    # 512-bit known prime for a stable, non-random benchmark
    p = int(
        "ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd1"
        "29024e088a67cc74020bbea63b139b22514a08798e3404dd"
        "ef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245"
        "e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7ed"
        "ee386bfb5a899fa5ae9f24117c4b1fe649286651ece65381"
        "ffffffffffffffff",
        16,
    )
    benchmark(is_prime, p)


def test_choose_prime_128(benchmark):
    benchmark(choose_prime, 128)


def test_choose_prime_256(benchmark):
    benchmark(choose_prime, 256)
