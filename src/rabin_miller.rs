use num_bigint::{BigUint, RandBigInt};
use num_traits::{One, Zero};
use rand::thread_rng;

pub fn is_prime(n: &BigUint, k: u32) -> bool {
    let zero = BigUint::zero();
    let one = BigUint::one();
    let two = BigUint::from(2u32);
    let three = BigUint::from(3u32);

    if n < &two {
        return false;
    }
    if n == &two || n == &three {
        return true;
    }
    if n % &two == zero {
        return false;
    }

    // Write n-1 as 2^r * d where d is odd
    let n_minus_1 = n - &one;
    let mut r = 0u32;
    let mut d = n_minus_1.clone();
    while &d % &two == BigUint::zero() {
        r += 1;
        d /= &two;
    }

    let mut rng = thread_rng();

    'outer: for _ in 0..k {
        let a = rng.gen_biguint_range(&two, &(n - &one));
        let mut x = a.modpow(&d, n);

        if x == one || x == n_minus_1 {
            continue;
        }

        for _ in 0..r - 1 {
            x = x.modpow(&two, n);
            if x == n_minus_1 {
                continue 'outer;
            }
        }
        return false;
    }

    true
}

pub fn get_random_odd_number(num_bits: usize) -> BigUint {
    assert!(num_bits > 1, "Number of bits must be at least 2");

    let mut rng = thread_rng();
    let lower = BigUint::one() << (num_bits - 2);
    let upper = (BigUint::one() << (num_bits - 1)) - BigUint::one();
    // gen_biguint_range is [lower, upper), so upper+1 to make it inclusive
    let r = rng.gen_biguint_range(&lower, &(upper + BigUint::one()));
    r * BigUint::from(2u32) + BigUint::one()
}

pub fn choose_prime(num_bits: usize) -> BigUint {
    let mut n = get_random_odd_number(num_bits);
    while !is_prime(&n, 5) {
        n = get_random_odd_number(num_bits);
    }
    n
}
