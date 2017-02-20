import random


"""

odd int n
n = (2^r)s + 1 --- s is odd
a: 1 <= a <= n -1
a^s = 1 mod n
or
a^(2js) = -1 mod n

"""

"""
single test: input: n, a

"""


def is_prime(n, threshold):
    # this should be repeated until enough a satidfy it

    # determined by threshold
    iterations = 5

    assert n >= 2
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # (2^r)*s = n -1
    tested_a = set()
    for i in range(iterations):
        a = random.randint(1, n - 1)
        while a in tested_a:
            a = random.randint(1, n - 1)
        tested_a.add(a)
        if not rabin_miller(n, a):
            return False
    return True


def rabin_miller(n, a):
    # find s
    s = n - 1
    r = 0
    # divmod?
    while (s % 2) == 0:
        s //= 2
        r += 1

    # will this handle large numbers?
    if (a ** s) % n == 1:
        return True

    for j in range(r):
        # bottleneck
        # 2^j can be calced by multilying by 2 each time
        if (a ** ((2 ** j) * s)) % n == n - 1:
            return True
    return False


for x in range(10000000, 10000010):
    print("{} is prime: {}".format(x, is_prime(x, 0)))

