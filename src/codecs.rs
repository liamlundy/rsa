use num_bigint::BigUint;

pub fn int_to_bytes(value: &BigUint) -> Vec<u8> {
    value.to_bytes_be()
}

pub fn bytes_to_int(bytes: &[u8]) -> BigUint {
    BigUint::from_bytes_be(bytes)
}
