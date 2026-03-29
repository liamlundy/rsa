def int_to_bytes(value: int) -> bytes:
    """
    Convert an integer to a byte array.

    Args:
        value (int): The input integer.
    Returns:
        bytes: The resulting byte array.
    """
    length = (value.bit_length() + 7) // 8  # calculate byte length
    return value.to_bytes(length, byteorder="big")


def bytes_to_int(byte_string: bytes) -> int:
    """
    Convert a byte array to an integer.

    Args:
        byte_string (bytes): The input byte array.
    Returns:
        int: The resulting integer.
    """
    return int.from_bytes(byte_string, byteorder="big")
