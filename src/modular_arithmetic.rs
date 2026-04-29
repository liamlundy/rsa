use num_bigint::BigInt;
use num_traits::{One, Zero};

/// Returns the modular inverse of `a` mod `m` using the Extended Euclidean Algorithm,
/// matching the Python implementation. Returns `None` if `gcd(a, m) != 1`.
pub fn mod_inv(a: &BigInt, m: &BigInt) -> Option<BigInt> {
    let zero = BigInt::zero();
    let one = BigInt::one();

    let mut u1 = one.clone();
    let mut u3 = a.clone();
    let mut v1 = zero.clone();
    let mut v3 = m.clone();

    while v3 != zero {
        let q = &u3 / &v3;
        let new_v1 = &u1 - &q * &v1;
        let new_v3 = &u3 - &q * &v3;
        u1 = v1;
        u3 = v3;
        v1 = new_v1;
        v3 = new_v3;
    }

    if u3 != one {
        return None;
    }

    Some(((u1 % m) + m) % m)
}
