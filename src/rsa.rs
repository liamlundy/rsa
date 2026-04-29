use num_bigint::{BigInt, BigUint, ToBigInt};
use num_traits::One;

use crate::codecs::{bytes_to_int, int_to_bytes};
use crate::modular_arithmetic::mod_inv;
use crate::rabin_miller::choose_prime;

/// Generate RSA key pair. Returns (e, d, n).
pub fn generate_keys(e: &BigUint, key_size: usize) -> (BigUint, BigUint, BigUint) {
    loop {
        let p = choose_prime(key_size / 2);
        let q = choose_prime(key_size / 2);
        let n = &p * &q;
        let totient = (&p - BigUint::one()) * (&q - BigUint::one());

        let e_int: BigInt = e.to_bigint().unwrap();
        let totient_int: BigInt = totient.to_bigint().unwrap();

        if let Some(d_int) = mod_inv(&e_int, &totient_int) {
            let d = d_int.to_biguint().unwrap();
            return (e.clone(), d, n);
        }
        // gcd(e, totient) != 1 — try new primes
    }
}

pub fn encrypt_value(plain_text: &BigUint, key: &BigUint, n: &BigUint) -> BigUint {
    plain_text.modpow(key, n)
}

pub fn decrypt_value(cipher_text: &BigUint, key: &BigUint, n: &BigUint) -> BigUint {
    cipher_text.modpow(key, n)
}

fn encrypt_chunk(chunk: &[u8], key: &BigUint, n: &BigUint, chunk_size: usize) -> Vec<u8> {
    let value = bytes_to_int(chunk);
    let encrypted = encrypt_value(&value, key, n);
    // Zero-pad to chunk_size so decryption can read fixed-size chunks
    let mut bytes = int_to_bytes(&encrypted);
    let pad = chunk_size.saturating_sub(bytes.len());
    let mut padded = vec![0u8; pad];
    padded.append(&mut bytes);
    padded
}

fn decrypt_chunk(chunk: &[u8], key: &BigUint, n: &BigUint) -> Vec<u8> {
    let value = bytes_to_int(chunk);
    let decrypted = decrypt_value(&value, key, n);
    int_to_bytes(&decrypted)
}

pub fn encrypt_bytes(plain_bytes: &[u8], key: &BigUint, n: &BigUint) -> Vec<u8> {
    let chunk_size = (n.bits() as usize + 7) / 8;
    let mut encrypted = Vec::new();
    for chunk in plain_bytes.chunks(chunk_size) {
        let enc = encrypt_chunk(chunk, key, n, chunk_size);
        encrypted.extend_from_slice(&enc);
    }
    encrypted
}

pub fn decrypt_bytes(encrypted_bytes: &[u8], key: &BigUint, n: &BigUint) -> Vec<u8> {
    let chunk_size = (n.bits() as usize + 7) / 8;
    let mut decrypted = Vec::new();
    for chunk in encrypted_bytes.chunks(chunk_size) {
        let dec = decrypt_chunk(chunk, key, n);
        decrypted.extend_from_slice(&dec);
    }
    decrypted
}
