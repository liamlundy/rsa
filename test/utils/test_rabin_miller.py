from utils.rabin_miller import is_prime


def test_is_prime():
    # THis should pass
    # assert is_prime(11)
    assert is_prime(101)
    assert not is_prime(10)
