use clap::{Parser, Subcommand};
use num_bigint::BigUint;
use std::fs;
use std::str::FromStr;

mod codecs;
mod modular_arithmetic;
mod rabin_miller;
mod rsa;

use rsa::{decrypt_bytes, encrypt_bytes, generate_keys};

#[derive(Parser)]
#[command(name = "rsa-cli", about = "RSA encryption CLI")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    GenerateKeys {
        #[arg(short = 'e', default_value_t = 65537u64, help = "Public exponent")]
        e: u64,
        #[arg(long, default_value_t = 2048usize, help = "Key size in bits")]
        key_size: usize,
        #[arg(long, default_value = "rsa_key", help = "Output filename prefix for keys")]
        key_name: String,
    },
    EncryptFile {
        #[arg(long, help = "Input file to encrypt")]
        input_file: String,
        #[arg(long, default_value = "encrypted.txt", help = "Output file for encrypted data")]
        output_file: String,
        #[arg(long, short = 'k', help = "Public key file for encryption")]
        public_key_file: String,
    },
    DecryptFile {
        #[arg(long, help = "Input file to decrypt")]
        input_file: String,
        #[arg(long, default_value = "decrypted.txt", help = "Output file for decrypted data")]
        output_file: String,
        #[arg(long, short = 'k', help = "Private key file for decryption")]
        private_key_file: String,
    },
}

fn read_key(path: &str) -> (BigUint, BigUint) {
    let content = fs::read_to_string(path).expect("Failed to read key file");
    let mut lines = content.lines();
    lines.next(); // skip header line ("Public Key" / "Private Key")
    let key = BigUint::from_str(lines.next().expect("Missing key value").trim())
        .expect("Invalid key value");
    let n = BigUint::from_str(lines.next().expect("Missing modulus").trim())
        .expect("Invalid modulus");
    (key, n)
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::GenerateKeys { e, key_size, key_name } => {
            let e_big = BigUint::from(e);
            let (e_key, d_key, n) = generate_keys(&e_big, key_size);

            fs::write(
                format!("{}.public", key_name),
                format!("Public Key\n{}\n{}\n", e_key, n),
            )
            .expect("Failed to write public key");

            fs::write(
                format!("{}.private", key_name),
                format!("Private Key\n{}\n{}\n", d_key, n),
            )
            .expect("Failed to write private key");

            println!("Keys generated and saved to {}", key_name);
        }

        Commands::EncryptFile { input_file, output_file, public_key_file } => {
            println!("Encrypting {} and saving to {}", input_file, output_file);
            let (public_key, n) = read_key(&public_key_file);
            let plaintext = fs::read_to_string(&input_file).expect("Failed to read input file");
            let encrypted = encrypt_bytes(plaintext.as_bytes(), &public_key, &n);
            fs::write(&output_file, &encrypted).expect("Failed to write encrypted file");
        }

        Commands::DecryptFile { input_file, output_file, private_key_file } => {
            println!("Decrypting {} and saving to {}", input_file, output_file);
            let (private_key, n) = read_key(&private_key_file);
            let encrypted = fs::read(&input_file).expect("Failed to read input file");
            let decrypted = decrypt_bytes(&encrypted, &private_key, &n);
            let text =
                String::from_utf8(decrypted).expect("Decrypted data is not valid UTF-8");
            println!("{}", text);
            fs::write(&output_file, &text).expect("Failed to write decrypted file");
        }
    }
}
