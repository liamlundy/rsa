import random


def is_prime(n):
    """

    :param n:
    :type n:
    :return:
    :rtype:
    """
    assert n >= 2

    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # for n < 2^64, these a are sufficient
    for a in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}:
        if not rabin_miller(n, a):
            return False
    return True


def rabin_miller(n, a):
    """

    :param n:
    :type n:
    :param a:
    :type a:
    :return:
    :rtype:
    """
    # find s, where n - 1 = s*2^r
    s = n - 1
    r = 0
    while (s % 2) == 0:
        s //= 2
        r += 1

    # a^s mod n = 1
    if pow(a, s, n) == 1:
        return True

    for j in range(r):
        # a^((2^j)*s) mod n = n - 1
        if pow(a, pow(2, j) * s, n) == n - 1:
            return True
    return False


# 512 bits each
def choose_prime():
    n = random.randint(2**511, 2**512)
    if n % 2 == 0:
        n += 1
    while not is_prime(n):
        n += 2
    return n
