from rsa.utils.codecs import bytes_to_int, int_to_bytes


class TestIntToBytes:
    def test_int_to_bytes(self):
        # TODO: make a better test
        assert int_to_bytes(0) == b""
        assert int_to_bytes(1) == b"\x01"
        assert int_to_bytes(1234) == b"\x04\xd2"
        assert int_to_bytes(123123123) == b"\x07V\xb5\xb3"


class TestBytesToInt:
    def test_bytes_to_int(self):
        assert bytes_to_int(b"") == 0
        assert bytes_to_int(b"\x01") == 1
        assert bytes_to_int(b"\x04\xd2") == 1234
        assert bytes_to_int(b"\x07V\xb5\xb3") == 123123123
