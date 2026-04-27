from math import gcd


def mod_inv(a: int, m: int) -> int:
    """
    Returns the modular inverse of a number.

    Args:
        a (int): The input number.
        m (int): The number to mod by.
    Returns:
        int: The inverse of (a mod m).
    """
    if gcd(a, m) != 1:
        raise ValueError(f"No mod inverse for {a} (mod {m})")
        # no mod inverse if a & m aren't relatively prime

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
