import pytest

from rsa.utils.rabin_miller import choose_prime, get_random_odd_number, is_prime


class TestIsPrime:
    def test_is_prime(self):
        assert not is_prime(-1)
        assert not is_prime(0)
        assert not is_prime(1)
        assert is_prime(2)
        assert is_prime(3)
        assert not is_prime(10)
        assert is_prime(11)
        assert is_prime(101)
        assert not is_prime(1000)


class TestGetRandomOddNumber:
    def test_get_random_odd_number_1_bit(self):
        num_bits = 1
        with pytest.raises(AssertionError):
            get_random_odd_number(num_bits)

    def test_get_random_odd_number_2_bit(self):
        for _ in range(100):
            num_bits = 2
            odd_number = get_random_odd_number(num_bits)
            assert odd_number % 2 == 1
            assert odd_number.bit_length() == num_bits

    def test_get_random_odd_number_5_bits(self):
        for _ in range(100):
            num_bits = 5
            odd_number = get_random_odd_number(num_bits)
            assert odd_number % 2 == 1
            assert odd_number.bit_length() == num_bits

    def test_get_random_odd_number_8_bits(self):
        for _ in range(100):
            num_bits = 8
            odd_number = get_random_odd_number(num_bits)
            assert odd_number % 2 == 1
            assert odd_number.bit_length() == num_bits

    def test_get_random_odd_number_512_bits(self):
        for _ in range(100):
            num_bits = 512
            odd_number = get_random_odd_number(num_bits)
            assert odd_number % 2 == 1
            assert odd_number.bit_length() == num_bits

    def test_get_random_odd_number_1024_bits(self):
        for _ in range(100):
            num_bits = 1024
            odd_number = get_random_odd_number(num_bits)
            assert odd_number % 2 == 1
            assert odd_number.bit_length() == num_bits


class TestChoosePrime:
    def test_choose_prime_2_bits(self):
        for _ in range(10):
            num_bits = 2
            prime = choose_prime(num_bits)
            assert prime.bit_length() == num_bits
            assert is_prime(prime)

    def test_choose_prime_6_bits(self):
        for _ in range(10):
            num_bits = 6
            prime = choose_prime(num_bits)
            assert prime.bit_length() == num_bits
            assert is_prime(prime)

    def test_choose_prime_16_bits(self):
        for _ in range(10):
            num_bits = 16
            prime = choose_prime(num_bits)
            assert prime.bit_length() == num_bits
            assert is_prime(prime)

    def test_choose_prime_512_bits(self):
        for _ in range(10):
            num_bits = 512
            prime = choose_prime(num_bits)
            assert prime.bit_length() == num_bits
            assert is_prime(prime)

    def test_choose_prime_1024_bits(self):
        for _ in range(10):
            num_bits = 1024
            prime = choose_prime(num_bits)
            assert prime.bit_length() == num_bits
            assert is_prime(prime)
