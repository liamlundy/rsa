from utils.rabin_miller import is_prime, choose_prime


def test_is_prime():
    # THis should pass
    # assert is_prime(11)
    assert is_prime(101)
    assert not is_prime(10)


def test_choose_prime():
    prime = choose_prime()
    assert is_prime(prime)
    assert 2 ** 511 <= prime
    assert 2 ** 512 >= prime


def test_choose_prime_with_values():
    prime = choose_prime(100, 300)
    assert is_prime(prime)
    assert 100 <= prime
    assert 300 >= prime


def test_choose_large_prime_with():
    prime = choose_prime(2 ** 1023, 2 ** 1024)
    assert is_prime(prime)
    assert 2 ** 1023 <= prime
    assert 2 ** 1024 >= prime
