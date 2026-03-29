import random


def is_prime(n: int, k: int = 5) -> bool:
    """
    Miller-Rabin primality test.

    Args:
        n: The number to test for primality.
        k: Number of rounds (higher = more accurate). Default is 10.
    Returns:
        True if n is probably prime, False if n is definitely composite.
    """
    # Handle base cases
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d where d is odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # Compute a^d mod n efficiently

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Definitely composite

    return True  # Probably prime


def get_random_odd_number(num_bits: int) -> int:
    """
    Generate a random odd number with the specified number of bits.

    Args:
        num_bits (int): The number of bits for the generated odd number.
    Returns:
        int: A random odd number with the specified number of bits.
    """
    assert num_bits > 1, "Number of bits must be at least 1"

    r = random.randint(2 ** (num_bits - 2), 2 ** (num_bits - 1) - 1)
    return r * 2 + 1


def choose_prime(num_bits: int = 512) -> int:
    """
    Choose a prime number with the specified number of bits.

    Args:
        num_bits (int): The number of bits for the generated prime number. Default
            is 512.
    Returns:
        int: A prime number with the specified number of bits.
    """
    # This generates a random odd number with the specified number of bits
    # generating until it finds a prime.
    n = get_random_odd_number(num_bits)
    while not is_prime(n):
        n = get_random_odd_number(num_bits)

    return n
