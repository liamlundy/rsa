from utils.codecs import encode_message, decode_message


def test_encode_message_english():
    test_string = '''English language test: abcdefghijklmnopqrstuvwxyz'''
    assert encode_message(test_string) == b'English language test: abcdefghijklmnopqrstuvwxyz'


def test_decode_message_english():
    test_bytes = b'English language test: abcdefghijklmnopqrstuvwxyz'
    assert decode_message(test_bytes) == '''English language test: abcdefghijklmnopqrstuvwxyz'''


def test_encode_message_arabic():
    # Change it to this string تم تكوين 1 فقرة، 5 كلمة، 27 بايت من نص لوريم إيبسوم
    test_string = '''المحتوى المقروء لصفحة ما سيلهي'''
    assert encode_message(test_string) == b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xad\xd8\xaa\xd9\x88\xd9\x89 \xd8\xa7\xd9\x84\xd9\x85\xd9\x82\xd8\xb1\xd9\x88\xd8\xa1 \xd9\x84\xd8\xb5\xd9\x81\xd8\xad\xd8\xa9 \xd9\x85\xd8\xa7 \xd8\xb3\xd9\x8a\xd9\x84\xd9\x87\xd9\x8a'


def test_decode_message_arabic():
    test_bytes = b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xad\xd8\xaa\xd9\x88\xd9\x89 \xd8\xa7\xd9\x84\xd9\x85\xd9\x82\xd8\xb1\xd9\x88\xd8\xa1 \xd9\x84\xd8\xb5\xd9\x81\xd8\xad\xd8\xa9 \xd9\x85\xd8\xa7 \xd8\xb3\xd9\x8a\xd9\x84\xd9\x87\xd9\x8a'
    assert decode_message(test_bytes) == '''المحتوى المقروء لصفحة ما سيلهي'''


def test_encode_symbols():
    assert True


def test_really_long():
    test_string = """
    This is a really long test string with numerous tabs     , newlines
    and random punctuation?!

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam varius facilisis tellus sit amet tempor. Etiam eu
    ligula a justo gravida pharetra. Cras faucibus mollis nisl. Sed fermentum interdum erat, in consectetur lorem
    faucibus eu. Nam malesuada, lectus vitae lacinia consequat, massa ex pretium sapien, et porttitor ante nulla eu
    risus. Morbi ac tellus fermentum, cursus ipsum vel, pharetra massa. Proin eu justo fringilla, faucibus magna sit
    amet, accumsan nisl. Vestibulum nec arcu at eros fringilla sagittis. Praesent ut magna scelerisque lorem sagittis
    iaculis. Maecenas at pellentesque neque, in dapibus lectus. Morbi a scelerisque tortor. Etiam varius tincidunt
    libero sit amet consectetur. Curabitur fringilla placerat augue, at ornare felis fermentum et.
    """
    encoded = encode_message(test_string)
    assert decode_message(encoded) == test_string