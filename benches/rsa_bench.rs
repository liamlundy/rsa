use criterion::{BenchmarkId, Criterion, criterion_group, criterion_main};
use num_bigint::BigUint;
use std::str::FromStr;

// Pull in the library modules directly from src/
#[path = "../src/codecs.rs"]
mod codecs;
#[path = "../src/modular_arithmetic.rs"]
mod modular_arithmetic;
#[path = "../src/rabin_miller.rs"]
mod rabin_miller;
#[path = "../src/rsa.rs"]
mod rsa;

use rabin_miller::{choose_prime, is_prime};
use rsa::{decrypt_bytes, encrypt_bytes, generate_keys};

const SHORT_MESSAGE: &[u8] = b"Hello, RSA benchmark!";
const LONG_MESSAGE: &[u8] = &[b'A'; 4096];

// ---------------------------------------------------------------------------
// Key generation
// ---------------------------------------------------------------------------

fn bench_keygen(c: &mut Criterion) {
    let e = BigUint::from(65537u32);
    let mut group = c.benchmark_group("keygen");
    for key_size in [512usize, 1024] {
        group.bench_with_input(
            BenchmarkId::from_parameter(format!("{key_size}bit")),
            &key_size,
            |b, &ks| b.iter(|| generate_keys(&e, ks)),
        );
    }
    group.finish();
}

// ---------------------------------------------------------------------------
// Encryption
// ---------------------------------------------------------------------------

fn bench_encrypt(c: &mut Criterion) {
    let e = BigUint::from(65537u32);
    let mut group = c.benchmark_group("encrypt");
    for key_size in [512usize, 1024, 2048] {
        let (pub_key, _, n) = generate_keys(&e, key_size);
        group.bench_with_input(
            BenchmarkId::new("short", format!("{key_size}bit")),
            &(&pub_key, &n),
            |b, (k, n)| b.iter(|| encrypt_bytes(SHORT_MESSAGE, k, n)),
        );
        group.bench_with_input(
            BenchmarkId::new("long_4k", format!("{key_size}bit")),
            &(&pub_key, &n),
            |b, (k, n)| b.iter(|| encrypt_bytes(LONG_MESSAGE, k, n)),
        );
    }
    group.finish();
}

// ---------------------------------------------------------------------------
// Decryption
// ---------------------------------------------------------------------------

fn bench_decrypt(c: &mut Criterion) {
    let e = BigUint::from(65537u32);
    let mut group = c.benchmark_group("decrypt");
    for key_size in [512usize, 1024, 2048] {
        let (pub_key, priv_key, n) = generate_keys(&e, key_size);
        let short_enc = encrypt_bytes(SHORT_MESSAGE, &pub_key, &n);
        let long_enc = encrypt_bytes(LONG_MESSAGE, &pub_key, &n);
        group.bench_with_input(
            BenchmarkId::new("short", format!("{key_size}bit")),
            &(&priv_key, &n, &short_enc),
            |b, (k, n, ct)| b.iter(|| decrypt_bytes(ct, k, n)),
        );
        group.bench_with_input(
            BenchmarkId::new("long_4k", format!("{key_size}bit")),
            &(&priv_key, &n, &long_enc),
            |b, (k, n, ct)| b.iter(|| decrypt_bytes(ct, k, n)),
        );
    }
    group.finish();
}

// ---------------------------------------------------------------------------
// Primality / prime generation
// ---------------------------------------------------------------------------

fn bench_is_prime(c: &mut Criterion) {
    // Small known prime
    let small_prime = BigUint::from(104729u32);
    // Large known prime (from RFC 3526 group 1, first 512-bit prime-like constant —
    // we use a genuine 512-bit prime for a non-trivial input)
    let large_prime = BigUint::from_str(
        "13220154346670377709146014335218272269600271839794188901918765166013660895971494940975527831098558965598009022945533897994842109350163702723",
    )
    .unwrap();

    let mut group = c.benchmark_group("is_prime");
    group.bench_function("small_104729", |b| b.iter(|| is_prime(&small_prime, 5)));
    group.bench_function("large_512bit", |b| b.iter(|| is_prime(&large_prime, 5)));
    group.finish();
}

fn bench_choose_prime(c: &mut Criterion) {
    let mut group = c.benchmark_group("choose_prime");
    for bits in [128usize, 256] {
        group.bench_with_input(
            BenchmarkId::from_parameter(format!("{bits}bit")),
            &bits,
            |b, &n| b.iter(|| choose_prime(n)),
        );
    }
    group.finish();
}

criterion_group!(
    benches,
    bench_keygen,
    bench_encrypt,
    bench_decrypt,
    bench_is_prime,
    bench_choose_prime
);
criterion_main!(benches);
