from codecs import decode, encode


def encode_message(plain):
    """
    Assumes its utf-8
    return an array of ints
    """

    return bytes(plain, 'utf-8')


def decode_message(encoded):
    """
    Takes an array of bytes
    return utf-8 text
    """
    hex_message = format(int(encode(encoded, 'hex'), 16), 'x')
    if (len(hex_message) % 2) != 0:
        hex_message = '0' + hex_message
    return decode(hex_message, 'hex').decode('utf-8')
