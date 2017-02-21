from numpy.core.test_rational import lcm
from math import gcd, log, ceil

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


def encrypt_block(message, key, n):
    # need to turn into ascii if letters
    # for now assume its a number
    assert message < n
    assert gcd(message, n) == 1
    return pow(message, key, n)


def encrypt_message(message, key, n):
    # TODO: Padding
    # TODO: Block size
    ciphertext = []
    # arbitrary block size of 8 that is relatively small
    for i in range(0, len(message), 8):
        ciphertext.append(encrypt_block(encode_block(message[i: min(i + 8, len(message))]), key, n))
    return ciphertext


def encode_block(text):
    # TODO: Handle unicode chars > 2 bytes
    result = 0
    shift = 8*(len(text) - 1)
    for letter in text:
        result += (ord(letter) << shift)
        shift -= 8
    return result


def decode_block(encoded):
    length = int(ceil(log(encoded, 16**2)))

    result = []
    shift = 8*(length - 1)
    for i in range(0, length):
        letter = (encoded >> shift)
        result.append(chr(letter))
        encoded = (encoded - (letter << shift))
        shift -= 8
    return ''.join(result)


def decrypt(ciphertext, key, n):
    plaintext = []
    for block in ciphertext:
        plaintext.append(decode_block(pow(block, key, n)))
    return ''.join(plaintext)

private, public, modulus = get_keys()
print("e: {}, \nd: {}, \nn: {}".format(private, public, modulus))

plain = """$$$$test

ꪪ

$%^
i am a test
woot"""

print("message: {}".format(plain))
ciph = encrypt_message(plain, public, modulus)
print("encrypt: {}".format(ciph))
plain = decrypt(ciph, private, modulus)
print("decrypt: {}".format(plain))