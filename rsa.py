import random
import utils

def generate_keypair(length):
    if length <= 1:
        raise ValueError("Key length too small")

    p = utils.generate_prime(length)
    q = utils.generate_prime(length)
    while q == p:
        q = utils.generate_prime(length)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(3, phi, 2)
        if utils.modexp(e, 2, phi) == 1:
            # skip if the inverse of e mod phi is e
            continue
        if utils.gcd(e, phi) == 1:
            break

    d = utils.modinv(e, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key

    N = utils.calculate_max_N(n)

    ord_message = []
    block = ""
    message = message.lower()
    for char in message:
        block += f"{ord(char) - 97:0{2}}"
        if len(block) >= 2 * N:
            ord_message.append(block)
            block = ""
    if block != "":
        while len(block) < 2 * N:
            # 99 - фіктивний символ
            block += "99"
        ord_message.append(block)

    return " ".join([str(utils.modexp(int(block), e, n)) for block in ord_message])

def decrypt_block(block, d, n):
    return pow(block, d, n)

def decrypt(message, private_key):
    d, n = private_key
    block_length = 2 * utils.calculate_max_N(n)

    decrypted_blocks = []
    for block in message.strip().split():
        decrypted_num = str(decrypt_block(int(block), d, n))
        # Pad the block with leading zeros
        decrypted_blocks.append(decrypted_num.zfill(block_length))

    all_numbers = ''.join(decrypted_blocks)
    plaintext = ""

    for i in range(0, len(all_numbers), 2):
        num = int(all_numbers[i:i+2])
        if 0 <= num <= 25:
            plaintext += chr(ord('A') + num)
        # Skip invalid numbers like 99, 98, etc.

    return plaintext
