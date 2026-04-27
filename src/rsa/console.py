import click

from .rsa import decrypt_bytes, encrypt_bytes
from .rsa import generate_keys as gen_keys

CHUNK_SIZE = 64


@click.group()
def cli():
    pass


@cli.command("generate-keys")
@click.option("-e", default=65537, help="Public exponent (default: 65537)", type=int)
@click.option(
    "--key-size", default=2048, help="Key size in bits (default: 2048)", type=int
)
@click.option(
    "--key-name", default="rsa_key", help="Output file for keys (default: rsa_key)"
)
def generate_keys(e: int, key_size: int, key_name: str):
    public_key, private_key, n = gen_keys(e=e, key_size=key_size)
    with open(f"{key_name}.public", "w") as f:
        f.write("Public Key\n")
        f.write(f"{public_key}\n")
        f.write(f"{n}\n")
    with open(f"{key_name}.private", "w") as f:
        f.write("Private Key\n")
        f.write(f"{private_key}\n")
        f.write(f"{n}\n")
    click.echo(f"Keys generated and saved to {key_name}")


@cli.command("encrypt-file")
@click.option("--input-file", required=True, help="Input file to encrypt")
@click.option(
    "--output-file", default="encrypted.txt", help="Output file for encrypted data"
)
@click.option(
    "--public-key-file", "-k", required=True, help="Public key file for encryption"
)
def encrypt_file(input_file: str, output_file: str, public_key_file: str):
    click.echo(f"Encrypting {input_file} and saving to {output_file}")
    with open(public_key_file, "r") as f:
        f.readline()
        public_key = int(f.readline().strip())
        n = int(f.readline().strip())
    with open(input_file, "r") as f:
        plaintext = f.read()  # string
        plain_bytes = plaintext.encode()  # bytes
    print(f"n ({n.bit_length() // 8}): {n}")
    encrypted = encrypt_bytes(plain_bytes, public_key, n)
    with open(output_file, "wb") as f:
        f.write(encrypted)


@cli.command("decrypt-file")
@click.option("--input-file", required=True, help="Input file to decrypt")
@click.option(
    "--output-file", default="decrypted.txt", help="Output file for decrypted data"
)
@click.option(
    "--private-key-file",
    "-k",
    required=True,
    help="Private key file path for decryption",
)
def decrypt_file(input_file: str, output_file: str, private_key_file: str):
    click.echo(f"Decrypting {input_file} and saving to {output_file}")
    with open(private_key_file, "r") as f:
        f.readline()
        private_key = int(f.readline().strip())
        n = int(f.readline().strip())
    with open(input_file, "rb") as f:
        encrypted = f.read()
    decrypted = decrypt_bytes(encrypted, private_key, n, chunk_size=CHUNK_SIZE * 8)
    print(decrypted)
    with open(output_file, "w") as f:
        f.write(decrypted.decode())


if __name__ == "__main__":
    cli()
