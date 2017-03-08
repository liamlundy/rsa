from codecs import decode, encode


def encode_message(plain):
    """
    utf-8 --> bytes
    Assumes its utf-8
    return an array of ints
    """

    return bytes(plain, 'utf-8')


def decode_message(encoded):
    """
    bytes --> utf-8
    Takes an array of bytes
    return utf-8 text
    """
    hex_message = format(int(encode(encoded, 'hex'), 16), 'x')
    if (len(hex_message) % 2) != 0:
        hex_message = '0' + hex_message
    return decode(hex_message, 'hex').decode('utf-8')


def int_to_bytes(integer):
    temp_bytes = format(integer, 'x')
    if (len(temp_bytes) % 2) != 0:
        temp_bytes = '0' + temp_bytes
    return decode(temp_bytes, 'hex')


def bytes_to_int(byte_string):
    return int(encode(byte_string, 'hex'), 16)
